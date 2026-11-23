"""Independent semantic audit shared by retained collection QA wrappers."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from kenken.cli import _atomic_write_many
from kenken.generation import evaluate_arithmetic_cage_policy, evaluate_difficulty
from kenken.model import CageV1, Grid
from kenken.serialization import parse_puzzle_bytes, parse_solution_bytes
from kenken.solver import verify

CAPS = {"easy": 4, "medium": 2, "hard": 1}
ARITHMETIC_LIMITS = {
    "max_add_target": 18,
    "max_add_terms": 3,
    "max_cage_cells": 3,
    "max_multiply_factors": 2,
    "max_multiply_target": 36,
}
GENERATION = {
    "arithmetic_cage_policy": {
        "applies_to_profiles": ["easy"],
        "limits": ARITHMETIC_LIMITS,
        "policy": "arithmetic-cap-v1",
    },
    "given_cage_policy": {
        "max_by_profile": CAPS,
        "policy": "given-cap-v1",
    },
    "max_attempts_per_puzzle": 2000,
    "max_solver_nodes": 1_000_000,
}


@dataclass(frozen=True)
class AuditSpec:
    volume: int
    seed_namespace: str
    pages: tuple[tuple[int, int, str, tuple[int, int, int, int]], ...]
    attempts: tuple[tuple[int, int, int, int], ...]
    prior_counts: tuple[int, ...]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _cage_satisfied(cage: CageV1, grid: Grid) -> bool:
    values = [grid[cell.row][cell.column] for cell in cage.cells]
    if cage.operator == "given":
        return len(values) == 1 and values[0] == cage.target
    if cage.operator == "add":
        return sum(values) == cage.target
    if cage.operator == "multiply":
        return math.prod(values) == cage.target
    if cage.operator == "subtract":
        return len(values) == 2 and abs(values[0] - values[1]) == cage.target
    high, low = max(values), min(values)
    return len(values) == 2 and high % low == 0 and high // low == cage.target


def _difficulty_stats(value: Any) -> dict[str, int]:
    return {
        "backtracks": value.backtracks,
        "max_decision_depth": value.max_decision_depth,
        "propagation_rounds": value.propagation_rounds,
        "visited_nodes": value.visited_nodes,
    }


def _prior_root(pdf_root: Path, volume: int) -> Path:
    return pdf_root if volume == 1 else pdf_root / f"volume-{volume}"


def _prior_manifest(pdf_root: Path, volume: int) -> Path:
    return _prior_root(pdf_root, volume) / "collection-manifest.json"


def _collection_ids(root: Path, manifest_path: Path) -> set[str]:
    manifest: dict[str, Any] = json.loads(manifest_path.read_text())
    ids: set[str] = set()
    for page in manifest["pages"]:
        for record in page["puzzles"]:
            puzzle_path = (root / record["puzzle_file"]).resolve()
            _require(
                puzzle_path.is_relative_to(root.resolve()), "prior puzzle path escape"
            )
            puzzle = parse_puzzle_bytes(puzzle_path.read_bytes())
            _require(puzzle.id == record["puzzle_id"], "prior manifest ID mismatch")
            _require(puzzle.id not in ids, "duplicate within prior")
            ids.add(puzzle.id)
    return ids


def audit_collection(root: Path, spec: AuditSpec) -> None:
    pdf_root = root / "output" / "pdf"
    package_root = pdf_root / f"volume-{spec.volume}"
    manifest_path = package_root / "collection-manifest.json"
    result_path = package_root / "qa" / "audit-results.json"
    manifest: dict[str, Any] = json.loads(manifest_path.read_text())

    collection_schema = json.loads(
        (root / "schemas" / "kenken-collection-manifest-v3.schema.json").read_text()
    )
    report_schema = json.loads(
        (root / "schemas" / "kenken-generation-report-v3.schema.json").read_text()
    )
    Draft202012Validator.check_schema(collection_schema)
    Draft202012Validator.check_schema(report_schema)
    Draft202012Validator(collection_schema).validate(manifest)
    report_validator = Draft202012Validator(report_schema)

    puzzle_count = sum(len(row[3]) for row in spec.pages)
    source_count = 3 * puzzle_count
    declared_count = source_count + len(spec.pages) + 1
    _require(puzzle_count == 28, "expected 28 puzzles")
    _require(declared_count == 92, "expected 92 declared artifacts")
    _require(manifest["schema"] == "kenken.collection-manifest/v3", "manifest schema")
    _require(manifest["volume"] == spec.volume, "manifest volume")
    _require(
        manifest["collection_pdf"]
        == f"../kenken-28-puzzle-collection-a4-volume-{spec.volume}.pdf",
        "combined PDF path",
    )
    _require(
        manifest["generation"] == {**GENERATION, "seed_namespace": spec.seed_namespace},
        "generation contract",
    )
    _require(
        manifest["page_geometry_points"]
        == {"height": "841.89", "width": "595.276"},
        "page geometry",
    )

    prior_ids: set[str] = set()
    expected_prior_records = []
    for volume, expected_count in enumerate(spec.prior_counts, start=1):
        root_for_prior = _prior_root(pdf_root, volume)
        manifest_for_prior = _prior_manifest(pdf_root, volume)
        collection_ids = _collection_ids(root_for_prior, manifest_for_prior)
        _require(len(collection_ids) == expected_count, f"Volume {volume} count")
        _require(not (prior_ids & collection_ids), "duplicate across prior collections")
        prior_ids.update(collection_ids)
        expected_prior_records.append(
            {
                "manifest": (
                    "../collection-manifest.json"
                    if volume == 1
                    else f"../volume-{volume}/collection-manifest.json"
                ),
                "puzzle_count": expected_count,
                "volume": volume,
            }
        )
    _require(
        manifest["cross_volume"]
        == {
            "distinct_from_priors": True,
            "prior_collections": expected_prior_records,
            "prior_puzzle_count": sum(spec.prior_counts),
        },
        "cross-volume contract",
    )

    expected_members = {
        f"../kenken-28-puzzle-collection-a4-volume-{spec.volume}.pdf"
    }
    for number, size, profile, seeds in spec.pages:
        expected_members.add(
            f"kenken-page-{number:02d}-{size}x{size}-{profile}-a4.pdf"
        )
        for ordinal, seed in enumerate(seeds, start=1):
            stem = (
                f"sources/page-{number:02d}-{size}x{size}-{profile}"
                f"-puzzle-{ordinal:02d}-seed-{seed}"
            )
            expected_members.update(
                {f"{stem}.puzzle.json", f"{stem}.solution.json", f"{stem}.report.json"}
            )
    declared: dict[str, str] = manifest["artifact_sha256"]
    _require(set(declared) == expected_members, "artifact membership")
    _require(len(declared) == declared_count, "artifact count")
    mismatches = [
        relative
        for relative, expected in declared.items()
        if not (package_root / relative).is_file()
        or _sha256(package_root / relative) != expected
    ]
    _require(not mismatches, f"artifact hash mismatches: {mismatches}")

    new_ids: set[str] = set()
    page_results: list[dict[str, object]] = []
    cages_checked = 0
    for page, expected, expected_attempts in zip(
        manifest["pages"], spec.pages, spec.attempts, strict=True
    ):
        number, size, profile, seeds = expected
        _require(
            (page["page_number"], page["size"], page["profile"])
            == (number, size, profile),
            f"page {number} specification",
        )
        _require(
            page["page_pdf"]
            == f"kenken-page-{number:02d}-{size}x{size}-{profile}-a4.pdf",
            f"page {number} PDF",
        )
        _require(len(page["puzzles"]) == 4, f"page {number} puzzle count")
        _require(
            tuple(record["ordinal"] for record in page["puzzles"]) == (1, 2, 3, 4),
            f"page {number} ordinals",
        )
        _require(
            tuple(record["seed"] for record in page["puzzles"])
            == tuple(str(seed) for seed in seeds),
            f"page {number} seeds",
        )
        _require(
            tuple(record["accepted_attempt"] for record in page["puzzles"])
            == expected_attempts,
            f"page {number} accepted attempts",
        )
        given_counts: list[int] = []
        for record in page["puzzles"]:
            puzzle = parse_puzzle_bytes(
                (package_root / record["puzzle_file"]).read_bytes()
            )
            solution = parse_solution_bytes(
                (package_root / record["solution_file"]).read_bytes(), puzzle
            )
            report = json.loads((package_root / record["report_file"]).read_text())
            report_validator.validate(report)
            _require(puzzle.id == record["puzzle_id"], f"{puzzle.id} manifest ID")
            _require(puzzle.id not in prior_ids, f"cross-volume duplicate {puzzle.id}")
            _require(puzzle.id not in new_ids, f"Volume duplicate {puzzle.id}")
            _require(puzzle.size == size, f"{puzzle.id} size")
            _require(puzzle.provenance is not None, f"{puzzle.id} provenance")
            assert puzzle.provenance is not None
            _require(
                (
                    puzzle.provenance.generator_version,
                    puzzle.provenance.profile,
                    puzzle.provenance.seed,
                    puzzle.provenance.accepted_attempt,
                )
                == (
                    "0.3.0",
                    profile,
                    record["seed"],
                    record["accepted_attempt"],
                ),
                f"{puzzle.id} provenance",
            )

            verified, solve_result = verify(puzzle, 1_000_000)
            _require(
                verified is not None and solve_result.status == "unique",
                f"{puzzle.id} uniqueness",
            )
            assert verified is not None
            _require(solution.grid == verified.solution, f"{puzzle.id} solution")
            symbols = set(range(1, size + 1))
            _require(
                all(set(row) == symbols for row in verified.solution),
                f"{puzzle.id} Latin rows",
            )
            _require(
                all(
                    {verified.solution[row][column] for row in range(size)} == symbols
                    for column in range(size)
                ),
                f"{puzzle.id} Latin columns",
            )
            _require(
                all(_cage_satisfied(cage, verified.solution) for cage in puzzle.cages),
                f"{puzzle.id} cage arithmetic",
            )
            cages_checked += len(puzzle.cages)

            difficulty = evaluate_difficulty(puzzle, 1_000_000)
            _require(
                difficulty is not None
                and difficulty.policy == "search-v1"
                and difficulty.band == profile,
                f"{puzzle.id} difficulty",
            )
            assert difficulty is not None
            given_count = sum(cage.operator == "given" for cage in puzzle.cages)
            _require(given_count <= CAPS[profile], f"{puzzle.id} given cap")
            _require(given_count == record["given_cages"], f"{puzzle.id} given record")
            arithmetic = evaluate_arithmetic_cage_policy(size, profile, puzzle.cages)
            _require(arithmetic.qualified, f"{puzzle.id} arithmetic policy")

            _require(report["schema"] == "kenken.generation-report/v3", "report schema")
            _require(report["size"] == size, f"{puzzle.id} report size")
            _require(report["seed"] == record["seed"], f"{puzzle.id} report seed")
            _require(report["requested_profile"] == profile, f"{puzzle.id} report profile")
            verified_attempts = report["attempts"]
            _require(
                verified_attempts == record["accepted_attempt"],
                f"{puzzle.id} report attempts",
            )
            _require(
                report["accepted_attempt"] == record["accepted_attempt"],
                f"{puzzle.id} report attempt",
            )
            _require(
                report["evaluated_difficulty"]
                == {
                    "band": difficulty.band,
                    "policy": difficulty.policy,
                    "stats": _difficulty_stats(difficulty.stats),
                },
                f"{puzzle.id} report difficulty",
            )
            _require(
                report["given_cage_policy"]
                == {
                    "accepted_given_cages": given_count,
                    "max_given_cages": CAPS[profile],
                    "policy": "given-cap-v1",
                },
                f"{puzzle.id} report given policy",
            )
            observed_maxima = {
                key: getattr(arithmetic.observed_maxima, key)
                for key in ARITHMETIC_LIMITS
            }
            limits = (
                {
                    key: getattr(arithmetic.limits, key)
                    for key in ARITHMETIC_LIMITS
                }
                if arithmetic.limits is not None
                else None
            )
            _require(
                report["arithmetic_cage_policy"]
                == {
                    "accepted_maxima": observed_maxima,
                    "applicable": profile == "easy",
                    "limits": limits,
                    "policy": "arithmetic-cap-v1",
                },
                f"{puzzle.id} report arithmetic policy",
            )
            _require(
                sum(report["rejection_counts"].values())
                == verified_attempts - 1,
                f"{puzzle.id} rejection accounting",
            )
            new_ids.add(puzzle.id)
            given_counts.append(given_count)
        page_results.append(
            {
                "given_cap": CAPS[profile],
                "given_counts": given_counts,
                "page": number,
                "profile": profile,
                "size": size,
            }
        )

    _require(len(new_ids) == puzzle_count, "new puzzle ID count")
    _require(
        len(prior_ids | new_ids) == sum(spec.prior_counts) + puzzle_count,
        "all-volume puzzle ID count",
    )
    _require(
        len(tuple((package_root / "sources").glob("*.json"))) == source_count,
        "source JSON count",
    )
    result = {
        "all_volume_puzzle_ids": len(prior_ids | new_ids),
        "cages_checked": cages_checked,
        "manifest_hashes_checked": len(declared),
        "page_results": page_results,
        "prior_puzzle_ids": len(prior_ids),
        "puzzles_checked": len(new_ids),
        "schema": f"kenken.volume-{spec.volume}-audit/v1",
        "source_json_checked": source_count,
        "status": "PASS",
    }
    data = (json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode()
    _atomic_write_many([(result_path, data)])
    print(
        f"PASS: Volume {spec.volume}, {len(new_ids)} puzzles, "
        f"{cages_checked} cages, {len(prior_ids | new_ids)} cross-volume IDs"
    )
