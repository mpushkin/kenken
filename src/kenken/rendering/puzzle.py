"""Puzzle board geometry and print styles."""

from __future__ import annotations

from dataclasses import dataclass

from kenken.model import Grid, VerifiedPuzzle
from kenken.rendering.scene import WHITE, Color, FillRect, Scene, StrokePath
from kenken.rendering.typography import (
    DIVISION,
    MINUS,
    MULTIPLICATION,
    add_centered_text,
    add_text,
    text_width,
)
from kenken.validation import validate_solution_grid

INK: Color = (24, 36, 54)
GRID: Color = (188, 196, 207)
ANSWER: Color = (52, 84, 119)
COORDINATE: Color = (67, 77, 91)
CAGE_FILLS: tuple[Color, ...] = (
    (235, 246, 235),
    (232, 243, 251),
    (243, 237, 250),
    (252, 244, 225),
    (251, 235, 238),
)

_CELL_SIZE = 1_000
_GUTTER = 360
_OPERATOR_GLYPH = {
    "add": "+",
    "subtract": MINUS,
    "multiply": MULTIPLICATION,
    "divide": DIVISION,
}


@dataclass(frozen=True)
class BoardStyle:
    cage_fills: bool
    grid_width: int
    cage_width: int
    border_width: int


STANDALONE_STYLE = BoardStyle(
    cage_fills=False,
    grid_width=8,
    cage_width=28,
    border_width=34,
)
SHEET_STYLE = BoardStyle(
    cage_fills=True,
    grid_width=14,
    cage_width=40,
    border_width=48,
)


def puzzle_scene(
    verified: VerifiedPuzzle,
    solution: Grid | None = None,
    *,
    style: BoardStyle = STANDALONE_STYLE,
) -> Scene:
    puzzle = verified.definition
    if solution is not None:
        validate_solution_grid(puzzle, solution)
        if solution != verified.solution:
            raise ValueError("solution does not match the verified unique solution")

    grid_extent = puzzle.size * _CELL_SIZE
    extent = _GUTTER + grid_extent + 60
    scene = Scene(extent, extent)
    scene.operations.append(FillRect(0, 0, extent, extent, WHITE))

    cage_by_cell = {
        (cell.row, cell.column): cage_index
        for cage_index, cage in enumerate(puzzle.cages)
        for cell in cage.cells
    }
    cage_colors = _cage_colors(verified) if style.cage_fills else ()
    if style.cage_fills:
        for row in range(puzzle.size):
            for column in range(puzzle.size):
                scene.operations.append(
                    FillRect(
                        _GUTTER + column * _CELL_SIZE,
                        _GUTTER + row * _CELL_SIZE,
                        _CELL_SIZE,
                        _CELL_SIZE,
                        cage_colors[cage_by_cell[(row, column)]],
                    )
                )

    # The neutral cell grid is deliberately subordinate to cage geometry.
    for index in range(1, puzzle.size):
        coordinate = _GUTTER + index * _CELL_SIZE
        scene.operations.append(
            StrokePath(
                ((_GUTTER, coordinate), (_GUTTER + grid_extent, coordinate)),
                style.grid_width,
                GRID,
            )
        )
        scene.operations.append(
            StrokePath(
                ((coordinate, _GUTTER), (coordinate, _GUTTER + grid_extent)),
                style.grid_width,
                GRID,
            )
        )

    cage_edges: set[tuple[int, int, int, int]] = set()
    for row in range(puzzle.size):
        for column in range(puzzle.size):
            cage_index = cage_by_cell[(row, column)]
            left = _GUTTER + column * _CELL_SIZE
            top = _GUTTER + row * _CELL_SIZE
            if row > 0 and cage_by_cell[(row - 1, column)] != cage_index:
                cage_edges.add((left, top, left + _CELL_SIZE, top))
            if column > 0 and cage_by_cell[(row, column - 1)] != cage_index:
                cage_edges.add((left, top, left, top + _CELL_SIZE))
            if row + 1 < puzzle.size and cage_by_cell[(row + 1, column)] != cage_index:
                cage_edges.add((left, top + _CELL_SIZE, left + _CELL_SIZE, top + _CELL_SIZE))
            if column + 1 < puzzle.size and cage_by_cell[(row, column + 1)] != cage_index:
                cage_edges.add((left + _CELL_SIZE, top, left + _CELL_SIZE, top + _CELL_SIZE))
    for x1, y1, x2, y2 in sorted(cage_edges):
        scene.operations.append(StrokePath(((x1, y1), (x2, y2)), style.cage_width, INK))
    scene.operations.append(
        StrokePath(
            (
                (_GUTTER, _GUTTER),
                (_GUTTER + grid_extent, _GUTTER),
                (_GUTTER + grid_extent, _GUTTER + grid_extent),
                (_GUTTER, _GUTTER + grid_extent),
            ),
            style.border_width,
            INK,
            closed=True,
        )
    )

    # Coordinate labels are derived presentation data; puzzle coordinates stay 0-based.
    for index in range(puzzle.size):
        label = str(index + 1)
        add_centered_text(
            scene,
            label,
            _GUTTER + index * _CELL_SIZE + _CELL_SIZE // 2,
            95,
            190,
            COORDINATE,
            stroke_width=24,
        )
        add_centered_text(
            scene,
            label,
            _GUTTER // 2,
            _GUTTER + index * _CELL_SIZE + 405,
            190,
            COORDINATE,
            stroke_width=24,
        )

    if solution is not None:
        for row, values in enumerate(solution):
            for column, value in enumerate(values):
                label = str(value)
                add_centered_text(
                    scene,
                    label,
                    _GUTTER + column * _CELL_SIZE + _CELL_SIZE // 2,
                    _GUTTER + row * _CELL_SIZE + 390,
                    460,
                    ANSWER,
                    stroke_width=45,
                )

    # Clues are painted last within the board and retain visual priority.
    for cage in puzzle.cages:
        clue_cell = min(cage.cells)
        clue = str(cage.target)
        if cage.operator != "given":
            clue += _OPERATOR_GLYPH[cage.operator]
        clue_height = _clue_height(clue)
        add_text(
            scene,
            clue,
            _GUTTER + clue_cell.column * _CELL_SIZE + 80,
            _GUTTER + clue_cell.row * _CELL_SIZE + 75,
            clue_height,
            INK,
            stroke_width=max(24, clue_height // 8),
        )
    return scene


def _clue_height(clue: str) -> int:
    height = 225
    while text_width(clue, height) > 840:
        height -= 5
    return height


def _cage_colors(verified: VerifiedPuzzle) -> tuple[Color, ...]:
    """Color normalized cages without repeating a prior adjacent color."""
    puzzle = verified.definition
    cage_by_cell = {
        (cell.row, cell.column): cage_index
        for cage_index, cage in enumerate(puzzle.cages)
        for cell in cage.cells
    }
    colors: list[Color] = []
    for cage_index, cage in enumerate(puzzle.cages):
        previous_neighbors: set[int] = set()
        for cell in cage.cells:
            for row, column in (
                (cell.row - 1, cell.column),
                (cell.row + 1, cell.column),
                (cell.row, cell.column - 1),
                (cell.row, cell.column + 1),
            ):
                neighbor = cage_by_cell.get((row, column))
                if neighbor is not None and neighbor < cage_index:
                    previous_neighbors.add(neighbor)
        unavailable = {colors[index] for index in previous_neighbors}
        color = next(
            (candidate for candidate in CAGE_FILLS if candidate not in unavailable),
            CAGE_FILLS[cage_index % len(CAGE_FILLS)],
        )
        colors.append(color)
    return tuple(colors)
