"""Strict JSON readers, canonical writers, and content-derived puzzle IDs."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from typing import Any, Never

from kenken.model import (
    CageV1,
    CellV1,
    Grid,
    Operator,
    ProvenanceV1,
    PuzzleDefinitionV1,
    SolutionV1,
)
from kenken.validation import (
    ValidationError,
    normalize_cages,
    validate_puzzle_structure,
    validate_solution_grid,
)

_ID_RE = re.compile(r"kk-([3-9])x\1-[0-9a-f]{16}")
_SEED_RE = re.compile(r"(?:0|[1-9][0-9]{0,19})")
_PROFILE_RE = re.compile(r"[a-z][a-z0-9-]{0,31}")
_VERSION_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z.+-]{0,63}")
_UINT64_MAX = 2**64 - 1
_OPERATORS: set[str] = {"given", "add", "subtract", "multiply", "divide"}


class DuplicateKeyError(ValidationError):
    """JSON contains a duplicate object key."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _load_json(data: bytes) -> Any:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValidationError("JSON must be UTF-8 without a BOM")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValidationError("JSON must be valid UTF-8") from error
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except DuplicateKeyError:
        raise
    except (json.JSONDecodeError, RecursionError) as error:
        raise ValidationError(f"malformed JSON: {error}") from error


def _object(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{context} must be an object")
    return value


def _exact_fields(
    value: Mapping[str, Any],
    *,
    required: set[str],
    optional: set[str] | frozenset[str] = frozenset(),
    context: str,
) -> None:
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required - optional)
    if missing:
        raise ValidationError(f"{context} is missing field {missing[0]!r}")
    if unknown:
        raise ValidationError(f"{context} has unknown field {unknown[0]!r}")


def _string(value: Any, context: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{context} must be a string")
    return value


def _integer(value: Any, context: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{context} must be an integer")
    return value


def _array(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{context} must be an array")
    return value


def parse_puzzle_bytes(data: bytes) -> PuzzleDefinitionV1:
    """Parse, normalize, and structurally validate a v1 puzzle."""
    raw = _object(_load_json(data), "puzzle")
    _exact_fields(
        raw,
        required={"schema", "id", "size", "cages"},
        optional={"provenance"},
        context="puzzle",
    )
    schema = _string(raw["schema"], "schema")
    puzzle_id = _string(raw["id"], "id")
    size = _integer(raw["size"], "size")
    if not _ID_RE.fullmatch(puzzle_id):
        raise ValidationError("id has an invalid grammar")

    cages = tuple(
        _parse_cage(item, cage_index)
        for cage_index, item in enumerate(_array(raw["cages"], "cages"))
    )
    provenance = (
        _parse_provenance(raw["provenance"]) if "provenance" in raw else None
    )
    puzzle = PuzzleDefinitionV1(
        schema=schema,
        id=puzzle_id,
        size=size,
        cages=normalize_cages(cages),
        provenance=provenance,
    )
    _validate_provenance(provenance)
    validate_puzzle_structure(puzzle)
    return puzzle


def _parse_cage(value: Any, cage_index: int) -> CageV1:
    raw = _object(value, f"cage {cage_index}")
    _exact_fields(
        raw,
        required={"target", "operator", "cells"},
        context=f"cage {cage_index}",
    )
    operator_text = _string(raw["operator"], f"cage {cage_index} operator")
    if operator_text not in _OPERATORS:
        raise ValidationError(f"cage {cage_index} has an unsupported operator")
    operator: Operator = operator_text  # type: ignore[assignment]
    cells = tuple(
        _parse_cell(item, cage_index, cell_index)
        for cell_index, item in enumerate(_array(raw["cells"], f"cage {cage_index} cells"))
    )
    return CageV1(
        target=_integer(raw["target"], f"cage {cage_index} target"),
        operator=operator,
        cells=cells,
    )


def _parse_cell(value: Any, cage_index: int, cell_index: int) -> CellV1:
    raw = _object(value, f"cage {cage_index} cell {cell_index}")
    _exact_fields(
        raw,
        required={"row", "column"},
        context=f"cage {cage_index} cell {cell_index}",
    )
    return CellV1(
        row=_integer(raw["row"], f"cage {cage_index} cell {cell_index} row"),
        column=_integer(raw["column"], f"cage {cage_index} cell {cell_index} column"),
    )


def _parse_provenance(value: Any) -> ProvenanceV1:
    raw = _object(value, "provenance")
    _exact_fields(
        raw,
        required={"generator_version", "seed", "profile", "accepted_attempt"},
        context="provenance",
    )
    return ProvenanceV1(
        generator_version=_string(raw["generator_version"], "generator_version"),
        seed=_string(raw["seed"], "seed"),
        profile=_string(raw["profile"], "profile"),
        accepted_attempt=_integer(raw["accepted_attempt"], "accepted_attempt"),
    )


def _validate_provenance(provenance: ProvenanceV1 | None) -> None:
    if provenance is None:
        return
    if not _VERSION_RE.fullmatch(provenance.generator_version):
        raise ValidationError("generator_version has an invalid ASCII grammar")
    if not provenance.generator_version.isascii():
        raise ValidationError("generator_version must be ASCII")
    if not _SEED_RE.fullmatch(provenance.seed) or int(provenance.seed) > _UINT64_MAX:
        raise ValidationError("seed must be a decimal uint64 string")
    if not _PROFILE_RE.fullmatch(provenance.profile) or not provenance.profile.isascii():
        raise ValidationError("profile has an invalid ASCII grammar")
    if isinstance(provenance.accepted_attempt, bool) or provenance.accepted_attempt <= 0:
        raise ValidationError("accepted_attempt must be a positive integer")


def _identity_object(puzzle: PuzzleDefinitionV1) -> dict[str, Any]:
    cages = normalize_cages(puzzle.cages)
    return {
        "schema": puzzle.schema,
        "size": puzzle.size,
        "cages": [
            {
                "target": cage.target,
                "operator": cage.operator,
                "cells": [
                    {"row": cell.row, "column": cell.column} for cell in cage.cells
                ],
            }
            for cage in cages
        ],
    }


def _json_line(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode()


def canonical_identity_bytes(puzzle: PuzzleDefinitionV1) -> bytes:
    """Return exact v1 identity bytes, excluding id and provenance."""
    validate_puzzle_structure(puzzle, check_id=False)
    return _json_line(_identity_object(puzzle))


def compute_puzzle_id(puzzle: PuzzleDefinitionV1) -> str:
    digest = hashlib.sha256(canonical_identity_bytes(puzzle)).hexdigest()[:16]
    return f"kk-{puzzle.size}x{puzzle.size}-{digest}"


def serialize_puzzle_bytes(puzzle: PuzzleDefinitionV1) -> bytes:
    """Serialize a validated normalized puzzle with exactly one terminal LF."""
    _validate_provenance(puzzle.provenance)
    validate_puzzle_structure(puzzle)
    value = _identity_object(puzzle)
    value["id"] = puzzle.id
    if puzzle.provenance is not None:
        value["provenance"] = {
            "generator_version": puzzle.provenance.generator_version,
            "seed": puzzle.provenance.seed,
            "profile": puzzle.provenance.profile,
            "accepted_attempt": puzzle.provenance.accepted_attempt,
        }
    return _json_line(value)


def parse_solution_bytes(data: bytes, puzzle: PuzzleDefinitionV1) -> SolutionV1:
    """Parse and validate a matching v1 solution sidecar."""
    raw = _object(_load_json(data), "solution")
    _exact_fields(
        raw,
        required={"schema", "puzzle_id", "grid"},
        context="solution",
    )
    schema = _string(raw["schema"], "solution schema")
    if schema != "kenken.solution/v1":
        raise ValidationError("solution schema must be 'kenken.solution/v1'")
    puzzle_id = _string(raw["puzzle_id"], "puzzle_id")
    if puzzle_id != puzzle.id:
        raise ValidationError("solution puzzle_id does not match the puzzle")
    grid_rows = _array(raw["grid"], "grid")
    grid: Grid = tuple(
        tuple(
            _integer(item, f"grid[{row_index}][{column_index}]")
            for column_index, item in enumerate(_array(row, f"grid[{row_index}]"))
        )
        for row_index, row in enumerate(grid_rows)
    )
    validate_solution_grid(puzzle, grid)
    return SolutionV1(schema=schema, puzzle_id=puzzle_id, grid=grid)


def serialize_solution_bytes(solution: SolutionV1, puzzle: PuzzleDefinitionV1) -> bytes:
    """Serialize a validated matching solution sidecar."""
    if solution.schema != "kenken.solution/v1":
        raise ValidationError("solution schema must be 'kenken.solution/v1'")
    if solution.puzzle_id != puzzle.id:
        raise ValidationError("solution puzzle_id does not match the puzzle")
    validate_solution_grid(puzzle, solution.grid)
    return _json_line(
        {
            "schema": solution.schema,
            "puzzle_id": solution.puzzle_id,
            "grid": [list(row) for row in solution.grid],
        }
    )


def unreachable(value: Never) -> Never:
    """Help static checking when a future union member is added."""
    raise AssertionError(f"unreachable value: {value!r}")
