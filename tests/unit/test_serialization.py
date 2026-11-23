import json

import pytest

from kenken.model import CageV1, ProvenanceV1, PuzzleDefinitionV1
from kenken.serialization import (
    DuplicateKeyError,
    canonical_identity_bytes,
    compute_puzzle_id,
    parse_puzzle_bytes,
    serialize_puzzle_bytes,
)
from kenken.validation import ValidationError


def test_canonical_identity_golden_vector(unique_puzzle: PuzzleDefinitionV1) -> None:
    expected = (
        b'{"cages":[{"cells":[{"column":0,"row":0}],"operator":"given","target":1},'
        b'{"cells":[{"column":1,"row":0}],"operator":"given","target":2},'
        b'{"cells":[{"column":2,"row":0}],"operator":"given","target":3},'
        b'{"cells":[{"column":0,"row":1}],"operator":"given","target":2},'
        b'{"cells":[{"column":1,"row":1}],"operator":"given","target":3},'
        b'{"cells":[{"column":2,"row":1}],"operator":"given","target":1},'
        b'{"cells":[{"column":0,"row":2}],"operator":"given","target":3},'
        b'{"cells":[{"column":1,"row":2}],"operator":"given","target":1},'
        b'{"cells":[{"column":2,"row":2}],"operator":"given","target":2}],'
        b'"schema":"kenken.puzzle/v1","size":3}\n'
    )
    assert canonical_identity_bytes(unique_puzzle) == expected
    assert canonical_identity_bytes(unique_puzzle).endswith(b"\n")
    assert not canonical_identity_bytes(unique_puzzle).endswith(b"\n\n")
    assert compute_puzzle_id(unique_puzzle) == "kk-3x3-748280b20a5aba7e"


def test_normalization_and_provenance_do_not_change_identity(
    multiple_puzzle: PuzzleDefinitionV1,
) -> None:
    provenance = ProvenanceV1("1.2.3+dev", "18446744073709551615", "easy-v1", 7)
    reversed_puzzle = PuzzleDefinitionV1(
        schema=multiple_puzzle.schema,
        id=multiple_puzzle.id,
        size=multiple_puzzle.size,
        cages=tuple(
            CageV1(cage.target, cage.operator, tuple(reversed(cage.cells)))
            for cage in reversed(multiple_puzzle.cages)
        ),
        provenance=provenance,
    )
    assert canonical_identity_bytes(reversed_puzzle) == canonical_identity_bytes(
        multiple_puzzle
    )
    assert compute_puzzle_id(reversed_puzzle) == multiple_puzzle.id
    parsed = parse_puzzle_bytes(serialize_puzzle_bytes(reversed_puzzle))
    assert parsed.cages == multiple_puzzle.cages
    assert parsed.provenance == provenance


@pytest.mark.parametrize(
    ("data", "error"),
    [
        (b"{", "malformed JSON"),
        (b'{"schema":"x","schema":"y"}', "duplicate JSON key"),
        (
            b'{"schema":"kenken.puzzle/v1","id":"kk-3x3-0000000000000000",'
            b'"size":3,"cages":[],"extra":1}',
            "unknown field",
        ),
    ],
)
def test_strict_json_rejections(data: bytes, error: str) -> None:
    with pytest.raises(ValidationError, match=error):
        parse_puzzle_bytes(data)


def test_duplicate_key_has_specific_error() -> None:
    with pytest.raises(DuplicateKeyError):
        parse_puzzle_bytes(b'{"schema":"x","schema":"y"}')


def test_mismatched_id_is_rejected(unique_puzzle: PuzzleDefinitionV1) -> None:
    value = json.loads(serialize_puzzle_bytes(unique_puzzle))
    value["id"] = "kk-3x3-0000000000000000"
    with pytest.raises(ValidationError, match="does not match"):
        parse_puzzle_bytes(json.dumps(value).encode())


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("generator_version", "é"),
        ("seed", "01"),
        ("seed", "18446744073709551616"),
        ("profile", "Easy"),
        ("accepted_attempt", 0),
    ],
)
def test_invalid_provenance_is_rejected(
    unique_puzzle: PuzzleDefinitionV1, field: str, value: object
) -> None:
    raw = json.loads(serialize_puzzle_bytes(unique_puzzle))
    raw["provenance"] = {
        "generator_version": "1.0.0",
        "seed": "42",
        "profile": "easy",
        "accepted_attempt": 1,
    }
    raw["provenance"][field] = value
    with pytest.raises(ValidationError):
        parse_puzzle_bytes(json.dumps(raw).encode())


def test_bom_is_rejected(unique_puzzle: PuzzleDefinitionV1) -> None:
    with pytest.raises(ValidationError, match="without a BOM"):
        parse_puzzle_bytes(b"\xef\xbb\xbf" + serialize_puzzle_bytes(unique_puzzle))
