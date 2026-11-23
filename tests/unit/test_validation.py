import pytest
from hypothesis import given
from hypothesis import strategies as st

from kenken.model import CageV1, CellV1, PuzzleDefinitionV1
from kenken.serialization import compute_puzzle_id
from kenken.validation import (
    ValidationError,
    cage_satisfied,
    cage_tuples,
    validate_puzzle_structure,
)


def _identified(cages: list[CageV1]) -> PuzzleDefinitionV1:
    puzzle = PuzzleDefinitionV1("kenken.puzzle/v1", "placeholder", 3, tuple(cages))
    return PuzzleDefinitionV1(
        puzzle.schema, compute_puzzle_id(puzzle), puzzle.size, puzzle.cages
    )


def _givens_except(excluded: set[CellV1]) -> list[CageV1]:
    return [
        CageV1((cell.row + cell.column) % 3 + 1, "given", (cell,))
        for cell in (CellV1(row, column) for row in range(3) for column in range(3))
        if cell not in excluded
    ]


def test_duplicate_cell_is_rejected(unique_puzzle: PuzzleDefinitionV1) -> None:
    cages = [*unique_puzzle.cages, CageV1(1, "given", (CellV1(0, 0),))]
    puzzle = PuzzleDefinitionV1(unique_puzzle.schema, "placeholder", 3, tuple(cages))
    with pytest.raises(ValidationError, match="appears more than once"):
        validate_puzzle_structure(puzzle, check_id=False)


def test_disconnected_cage_is_rejected() -> None:
    cells = {CellV1(0, 0), CellV1(2, 2)}
    cages = [CageV1(2, "add", tuple(cells)), *_givens_except(cells)]
    puzzle = PuzzleDefinitionV1("kenken.puzzle/v1", "placeholder", 3, tuple(cages))
    with pytest.raises(ValidationError, match="not orthogonally connected"):
        validate_puzzle_structure(puzzle, check_id=False)


def test_oversized_cage_is_rejected_before_preprocessing() -> None:
    cells = {
        CellV1(0, 0),
        CellV1(0, 1),
        CellV1(0, 2),
        CellV1(1, 0),
        CellV1(1, 1),
    }
    cages = [CageV1(9, "add", tuple(cells)), *_givens_except(cells)]
    puzzle = PuzzleDefinitionV1("kenken.puzzle/v1", "placeholder", 3, tuple(cages))
    with pytest.raises(ValidationError, match=r"requires 2\.\.4 cells"):
        validate_puzzle_structure(puzzle, check_id=False)


@pytest.mark.parametrize(
    "cage",
    [
        CageV1(4, "given", (CellV1(0, 0),)),
        CageV1(7, "add", (CellV1(0, 0), CellV1(0, 1))),
        CageV1(3, "subtract", (CellV1(0, 0), CellV1(0, 1))),
        CageV1(10, "multiply", (CellV1(0, 0), CellV1(0, 1))),
        CageV1(4, "divide", (CellV1(0, 0), CellV1(0, 1))),
    ],
)
def test_target_bounds_are_rejected(cage: CageV1) -> None:
    cells = set(cage.cells)
    puzzle = PuzzleDefinitionV1(
        "kenken.puzzle/v1",
        "placeholder",
        3,
        tuple([cage, *_givens_except(cells)]),
    )
    with pytest.raises(ValidationError, match="target exceeds"):
        validate_puzzle_structure(puzzle, check_id=False)


def test_empty_legal_tuple_set_is_rejected() -> None:
    cells = {CellV1(0, 0), CellV1(0, 1)}
    cage = CageV1(2, "add", tuple(cells))
    puzzle = PuzzleDefinitionV1(
        "kenken.puzzle/v1",
        "placeholder",
        3,
        tuple([cage, *_givens_except(cells)]),
    )
    with pytest.raises(ValidationError, match="no legal satisfying tuples"):
        validate_puzzle_structure(puzzle, check_id=False)


def test_exact_order_independent_cage_predicates() -> None:
    assert cage_satisfied("subtract", 2, (2, 4))
    assert cage_satisfied("subtract", 2, (4, 2))
    assert cage_satisfied("divide", 2, (2, 4))
    assert cage_satisfied("divide", 2, (4, 2))
    assert not cage_satisfied("divide", 1, (2, 3))
    assert cage_satisfied("given", 3, (3,))
    assert cage_satisfied("add", 6, (1, 2, 3))
    assert cage_satisfied("multiply", 6, (1, 2, 3))


@given(
    left=st.integers(min_value=1, max_value=9),
    right=st.integers(min_value=1, max_value=9),
    target=st.integers(min_value=1, max_value=9),
)
def test_binary_predicates_are_invariant_under_reversal(
    left: int, right: int, target: int
) -> None:
    for operator in ("subtract", "divide"):
        assert cage_satisfied(operator, target, (left, right)) == cage_satisfied(
            operator, target, (right, left)
        )


def test_tuple_preprocessing_is_bounded_by_n_to_four() -> None:
    cage = CageV1(
        20,
        "add",
        (CellV1(0, 0), CellV1(1, 0), CellV1(2, 0), CellV1(3, 0)),
    )
    assert len(cage_tuples(9, cage)) <= 9**4
