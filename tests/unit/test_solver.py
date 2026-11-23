import itertools
from pathlib import Path

import pytest

from kenken.model import PuzzleDefinitionV1, SolverBudget
from kenken.serialization import parse_puzzle_bytes
from kenken.solver import solve, solve_one, verify
from kenken.validation import cage_satisfied

FIXTURES = Path(__file__).parents[1] / "fixtures" / "puzzles"


def test_unique_multiple_unsatisfiable_and_unknown(
    unique_puzzle: PuzzleDefinitionV1,
    multiple_puzzle: PuzzleDefinitionV1,
    unsatisfiable_puzzle: PuzzleDefinitionV1,
) -> None:
    unique = solve(unique_puzzle)
    assert unique.status == "unique"
    assert unique.solutions_found == 1
    assert unique.first_solution == ((1, 2, 3), (2, 3, 1), (3, 1, 2))

    multiple = solve(multiple_puzzle)
    assert multiple.status == "multiple"
    assert multiple.solutions_found == 2

    unsatisfiable = solve(unsatisfiable_puzzle)
    assert unsatisfiable.status == "unsatisfiable"
    assert unsatisfiable.solutions_found == 0

    unknown = solve(multiple_puzzle, max_solver_nodes=1)
    assert unknown.status == "unknown"
    assert unknown.solutions_found in (0, 1)
    assert unknown.stats.visited_nodes == 1


def test_deterministic_stats_and_fixed_root_semantics(
    unique_puzzle: PuzzleDefinitionV1,
    multiple_puzzle: PuzzleDefinitionV1,
) -> None:
    first = solve(multiple_puzzle)
    second = solve(multiple_puzzle)
    assert first == second
    assert first.stats.visited_nodes >= 3
    assert first.stats.max_decision_depth > 0

    given = solve(unique_puzzle)
    assert given.stats.visited_nodes == 1
    assert given.stats.max_decision_depth == 0
    assert given.stats.backtracks == 0
    assert given.stats.propagation_rounds == 2


def test_solve_one_has_independently_reset_telemetry(
    multiple_puzzle: PuzzleDefinitionV1,
) -> None:
    uniqueness = solve(multiple_puzzle)
    one = solve_one(multiple_puzzle)
    repeated = solve_one(multiple_puzzle)
    assert one == repeated
    assert one.status == "solved"
    assert one.solution is not None
    assert one.stats.visited_nodes < uniqueness.stats.visited_nodes


def test_verified_capability_only_for_unique(
    unique_puzzle: PuzzleDefinitionV1, multiple_puzzle: PuzzleDefinitionV1
) -> None:
    verified, result = verify(unique_puzzle)
    assert result.status == "unique"
    assert verified is not None
    assert verified.solution == result.first_solution

    unverified, result = verify(multiple_puzzle)
    assert result.status == "multiple"
    assert unverified is None


@pytest.mark.parametrize(
    "limit",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(True, id="boolean-true"),
        pytest.param(False, id="boolean-false"),
        pytest.param(1.5, id="fractional-float"),
        pytest.param(float("inf"), id="positive-infinity"),
        pytest.param(float("-inf"), id="negative-infinity"),
        pytest.param(float("nan"), id="nan"),
        pytest.param("10", id="string"),
        pytest.param(None, id="none"),
        pytest.param(object(), id="object"),
    ],
)
def test_all_public_solver_entry_points_require_positive_integer_limit(
    unique_puzzle: PuzzleDefinitionV1, limit: object
) -> None:
    with pytest.raises(ValueError, match="positive"):
        solve(unique_puzzle, limit)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="positive"):
        solve_one(unique_puzzle, limit)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="positive"):
        verify(unique_puzzle, limit)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="positive"):
        SolverBudget(limit)  # type: ignore[arg-type]


def _oracle_count(puzzle: PuzzleDefinitionV1) -> int:
    rows = tuple(itertools.permutations(range(1, puzzle.size + 1)))
    count = 0
    for candidate in itertools.product(rows, repeat=puzzle.size):
        if any(
            len({candidate[row][column] for row in range(puzzle.size)}) != puzzle.size
            for column in range(puzzle.size)
        ):
            continue
        if all(
            cage_satisfied(
                cage.operator,
                cage.target,
                tuple(candidate[cell.row][cell.column] for cell in cage.cells),
            )
            for cage in puzzle.cages
        ):
            count += 1
    return count


def test_3x3_solver_agrees_with_brute_force_oracle(
    unique_puzzle: PuzzleDefinitionV1,
    multiple_puzzle: PuzzleDefinitionV1,
    unsatisfiable_puzzle: PuzzleDefinitionV1,
) -> None:
    for puzzle in (unique_puzzle, multiple_puzzle, unsatisfiable_puzzle):
        oracle = _oracle_count(puzzle)
        result = solve(puzzle)
        expected = "unsatisfiable" if oracle == 0 else "unique" if oracle == 1 else "multiple"
        assert result.status == expected
        assert result.solutions_found == min(oracle, 2)


def test_operational_4x4_fixture_is_unique() -> None:
    puzzle = parse_puzzle_bytes((FIXTURES / "unique-4x4.json").read_bytes())
    result = solve(puzzle)
    assert result.status == "unique"
    assert result.first_solution == (
        (1, 2, 3, 4),
        (2, 3, 4, 1),
        (3, 4, 1, 2),
        (4, 1, 2, 3),
    )
