"""Domain invariants and shared cage arithmetic."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from itertools import product
from math import prod

from kenken.model import CageV1, CellV1, Grid, Operator, PuzzleDefinitionV1


class ValidationError(ValueError):
    """An input violates a v1 schema or domain invariant."""


def cage_satisfied(operator: Operator, target: int, values: Sequence[int]) -> bool:
    """Return whether values satisfy the authoritative v1 cage predicate."""
    if operator == "given":
        return len(values) == 1 and values[0] == target
    if operator == "add":
        return sum(values) == target
    if operator == "multiply":
        return prod(values) == target
    if operator == "subtract":
        return len(values) == 2 and abs(values[0] - values[1]) == target
    if operator == "divide":
        if len(values) != 2:
            return False
        left, right = values
        return (left % right == 0 and left // right == target) or (
            right % left == 0 and right // left == target
        )
    return False


def cage_tuples(size: int, cage: CageV1) -> tuple[tuple[int, ...], ...]:
    """Enumerate legal tuples in ascending product order (at most N^4 raw tuples)."""
    candidates: list[tuple[int, ...]] = []
    for values in product(range(1, size + 1), repeat=len(cage.cells)):
        if not cage_satisfied(cage.operator, cage.target, values):
            continue
        if _violates_internal_latin(cage.cells, values):
            continue
        candidates.append(values)
    return tuple(candidates)


def _violates_internal_latin(cells: Sequence[CellV1], values: Sequence[int]) -> bool:
    for left_index, left in enumerate(cells):
        for right_index in range(left_index + 1, len(cells)):
            right = cells[right_index]
            if (
                left.row == right.row or left.column == right.column
            ) and values[left_index] == values[right_index]:
                return True
    return False


def validate_puzzle_structure(puzzle: PuzzleDefinitionV1, *, check_id: bool = True) -> None:
    """Validate all non-search v1 puzzle invariants."""
    if puzzle.schema != "kenken.puzzle/v1":
        raise ValidationError("schema must be 'kenken.puzzle/v1'")
    if (
        isinstance(puzzle.size, bool)
        or not isinstance(puzzle.size, int)
        or not 3 <= puzzle.size <= 9
    ):
        raise ValidationError("size must be between 3 and 9")
    if not puzzle.cages:
        raise ValidationError("cages must not be empty")

    seen: set[CellV1] = set()
    for cage_index, cage in enumerate(puzzle.cages):
        _validate_cage(puzzle.size, cage, cage_index)
        for cell in cage.cells:
            if (
                isinstance(cell.row, bool)
                or not isinstance(cell.row, int)
                or isinstance(cell.column, bool)
                or not isinstance(cell.column, int)
            ):
                raise ValidationError(f"cage {cage_index} cell coordinates must be integers")
            if not (0 <= cell.row < puzzle.size and 0 <= cell.column < puzzle.size):
                raise ValidationError(f"cage {cage_index} contains an out-of-range cell")
            if cell in seen:
                raise ValidationError(f"cell ({cell.row}, {cell.column}) appears more than once")
            seen.add(cell)
        if not _orthogonally_connected(cage.cells):
            raise ValidationError(f"cage {cage_index} is not orthogonally connected")
        if not cage_tuples(puzzle.size, cage):
            raise ValidationError(f"cage {cage_index} has no legal satisfying tuples")

    expected = {
        CellV1(row, column)
        for row in range(puzzle.size)
        for column in range(puzzle.size)
    }
    missing = sorted(expected - seen)
    if missing:
        first = missing[0]
        raise ValidationError(f"cell ({first.row}, {first.column}) is not in any cage")

    if check_id:
        from kenken.serialization import compute_puzzle_id

        expected_id = compute_puzzle_id(puzzle)
        if puzzle.id != expected_id:
            raise ValidationError(
                f"id does not match canonical puzzle identity: expected {expected_id}"
            )


def _validate_cage(size: int, cage: CageV1, cage_index: int) -> None:
    cell_count = len(cage.cells)
    cardinalities = {
        "given": (1, 1),
        "subtract": (2, 2),
        "divide": (2, 2),
        "add": (2, 4),
        "multiply": (2, 4),
    }
    if cage.operator not in cardinalities:
        raise ValidationError(f"cage {cage_index} has an unsupported operator")
    minimum, maximum = cardinalities[cage.operator]
    if not minimum <= cell_count <= maximum:
        raise ValidationError(
            f"cage {cage_index} operator {cage.operator!r} requires "
            f"{minimum}" + (f"..{maximum}" if minimum != maximum else "") + " cells"
        )
    if (
        isinstance(cage.target, bool)
        or not isinstance(cage.target, int)
        or cage.target <= 0
    ):
        raise ValidationError(f"cage {cage_index} target must be a positive integer")

    bounds = {
        "given": size,
        "add": cell_count * size,
        "subtract": size - 1,
        "multiply": size**cell_count,
        "divide": size,
    }
    if cage.target > bounds[cage.operator]:
        raise ValidationError(
            f"cage {cage_index} target exceeds the {cage.operator!r} bound "
            f"of {bounds[cage.operator]}"
        )


def _orthogonally_connected(cells: Sequence[CellV1]) -> bool:
    if not cells:
        return False
    remaining = set(cells)
    frontier = [remaining.pop()]
    while frontier:
        cell = frontier.pop()
        neighbors = {
            CellV1(cell.row - 1, cell.column),
            CellV1(cell.row + 1, cell.column),
            CellV1(cell.row, cell.column - 1),
            CellV1(cell.row, cell.column + 1),
        }
        reached = remaining & neighbors
        remaining -= reached
        frontier.extend(reached)
    return not remaining


def validate_solution_grid(puzzle: PuzzleDefinitionV1, grid: Grid) -> None:
    """Validate dimensions, Latin constraints, and cages for a supplied solution."""
    size = puzzle.size
    if len(grid) != size or any(len(row) != size for row in grid):
        raise ValidationError(f"solution grid must be {size} by {size}")
    expected_values = set(range(1, size + 1))
    for row_index, row in enumerate(grid):
        if any(isinstance(value, bool) or value not in expected_values for value in row):
            raise ValidationError(f"solution row {row_index} contains an out-of-range value")
        if set(row) != expected_values:
            raise ValidationError(f"solution row {row_index} is not a Latin permutation")
    for column in range(size):
        column_values = {grid[row][column] for row in range(size)}
        if column_values != expected_values:
            raise ValidationError(f"solution column {column} is not a Latin permutation")
    for cage_index, cage in enumerate(puzzle.cages):
        cage_values = tuple(grid[cell.row][cell.column] for cell in cage.cells)
        if not cage_satisfied(cage.operator, cage.target, cage_values):
            raise ValidationError(f"solution does not satisfy cage {cage_index}")


def normalize_cells(cells: Iterable[CellV1]) -> tuple[CellV1, ...]:
    return tuple(sorted(cells))


def normalize_cages(cages: Iterable[CageV1]) -> tuple[CageV1, ...]:
    normalized = [
        CageV1(cage.target, cage.operator, normalize_cells(cage.cells)) for cage in cages
    ]
    return tuple(sorted(normalized, key=lambda cage: cage.cells[0]))
