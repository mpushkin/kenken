import json
from pathlib import Path

import pytest

from kenken.model import PuzzleDefinitionV1
from kenken.serialization import parse_solution_bytes
from kenken.validation import ValidationError

FIXTURES = Path(__file__).parents[1] / "fixtures"


def test_valid_solution_sidecar(unique_puzzle: PuzzleDefinitionV1) -> None:
    solution = parse_solution_bytes(
        (FIXTURES / "solutions" / "unique-3x3.json").read_bytes(),
        unique_puzzle,
    )
    assert solution.grid == ((1, 2, 3), (2, 3, 1), (3, 1, 2))


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("puzzle_id", "kk-3x3-0000000000000000", "does not match"),
        ("grid", [[1, 2], [2, 3]], "3 by 3"),
        ("grid", [[1, 1, 3], [2, 3, 1], [3, 2, 2]], "not a Latin"),
        ("grid", [[1, 2, 3], [2, 3, 1], [3, 2, 1]], "not a Latin"),
    ],
)
def test_invalid_solution_sidecar(
    unique_puzzle: PuzzleDefinitionV1, field: str, value: object, error: str
) -> None:
    raw = {
        "schema": "kenken.solution/v1",
        "puzzle_id": unique_puzzle.id,
        "grid": [[1, 2, 3], [2, 3, 1], [3, 1, 2]],
    }
    raw[field] = value
    with pytest.raises(ValidationError, match=error):
        parse_solution_bytes(json.dumps(raw).encode(), unique_puzzle)

