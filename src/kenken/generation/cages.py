"""Connected cage construction and target selection."""

from __future__ import annotations

from math import prod

from kenken.generation.arithmetic_policy import (
    arithmetic_clue_allowed,
    cage_size_allowed,
)
from kenken.generation.given_policy import given_cage_cap
from kenken.model import CageV1, CellV1, DifficultyBand, Grid, Operator
from kenken.randomness import RandomV1
from kenken.validation import normalize_cages

_SIZE_CHOICES: dict[DifficultyBand, tuple[int, ...]] = {
    "easy": (1, 2, 2, 2, 3, 3, 4, 4),
    "medium": (1, 2, 2, 3, 3, 4),
    "hard": (2, 3, 3, 4, 4, 4),
}


def build_cages(
    grid: Grid,
    profile: DifficultyBand,
    random: RandomV1,
    enabled_operations: tuple[Operator, ...],
) -> tuple[CageV1, ...]:
    size = len(grid)
    remaining = {CellV1(row, column) for row in range(size) for column in range(size)}
    cages: list[CageV1] = []
    completed_singletons = 0
    given_limit = given_cage_cap(size, profile)
    while remaining:
        roots = sorted(remaining)
        root = roots[random.randbelow(len(roots))]
        size_choices = tuple(
            choice
            for choice in _SIZE_CHOICES[profile]
            if cage_size_allowed(size, profile, choice, enabled_operations)
        )
        if completed_singletons >= given_limit:
            size_choices = tuple(choice for choice in size_choices if choice != 1)
        wanted = random.choice(size_choices)
        cells = [root]
        remaining.remove(root)
        while len(cells) < wanted:
            frontier = sorted(
                {
                    neighbor
                    for cell in cells
                    for neighbor in _neighbors(cell, size)
                    if neighbor in remaining
                }
            )
            if not frontier:
                break
            selected = frontier[random.randbelow(len(frontier))]
            cells.append(selected)
            remaining.remove(selected)
        if len(cells) == 1:
            completed_singletons += 1
        cages.append(
            _cage_for_cells(
                grid,
                tuple(sorted(cells)),
                profile,
                random,
                enabled_operations,
            )
        )
    return normalize_cages(cages)


def _neighbors(cell: CellV1, size: int) -> tuple[CellV1, ...]:
    return tuple(
        candidate
        for candidate in (
            CellV1(cell.row - 1, cell.column),
            CellV1(cell.row + 1, cell.column),
            CellV1(cell.row, cell.column - 1),
            CellV1(cell.row, cell.column + 1),
        )
        if 0 <= candidate.row < size and 0 <= candidate.column < size
    )


def _cage_for_cells(
    grid: Grid,
    cells: tuple[CellV1, ...],
    profile: DifficultyBand,
    random: RandomV1,
    enabled_operations: tuple[Operator, ...],
) -> CageV1:
    values = tuple(grid[cell.row][cell.column] for cell in cells)
    if len(cells) == 1:
        return CageV1(values[0], "given", cells)
    choices: list[tuple[Operator, int]] = [("add", sum(values)), ("multiply", prod(values))]
    if len(cells) == 2:
        left, right = values
        choices.append(("subtract", abs(left - right)))
        large, small = max(values), min(values)
        if large % small == 0:
            choices.append(("divide", large // small))
    choices = [
        choice
        for choice in choices
        if choice[1] > 0
        and choice[0] in enabled_operations
        and arithmetic_clue_allowed(
            len(grid), profile, choice[0], choice[1], len(cells)
        )
    ]
    if profile == "easy":
        choices.extend(
            choice for choice in tuple(choices) if choice[0] in ("subtract", "divide")
        )
    elif profile == "hard":
        choices.extend(choice for choice in tuple(choices) if choice[0] == "multiply")
    operator, target = random.choice(choices)
    return CageV1(target, operator, cells)
