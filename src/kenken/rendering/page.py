"""Printable A4 and Letter page composition."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from kenken.model import VerifiedPuzzle
from kenken.rendering.puzzle import INK, SHEET_STYLE, puzzle_scene
from kenken.rendering.scene import WHITE, Color, FillRect, Scene, StrokePath, place_scene
from kenken.rendering.typography import (
    MULTIPLICATION,
    add_centered_friendly_title,
    add_centered_proportional_text,
    add_text,
    text_width,
)

type Paper = Literal["a4", "letter"]
type Layout = Literal["2up", "4up"]

PAPER_SIZES: dict[Paper, tuple[int, int]] = {
    "a4": (595_276, 841_890),
    "letter": (612_000, 792_000),
}

_PANEL_ACCENTS: tuple[Color, ...] = (
    (57, 133, 81),
    (45, 112, 174),
    (119, 79, 160),
    (218, 126, 43),
)
_INSTRUCTION = (
    "Use 1 through N once in every row and every column.",
    "Make each cage reach its target with the operation shown.",
)


def standalone_page(puzzle: Scene) -> Scene:
    page = Scene(432_000, 432_000)
    page.operations.append(FillRect(0, 0, page.width, page.height, WHITE))
    place_scene(puzzle, page, 18_000, 18_000, 396_000, 396_000)
    return page


def compose_page(puzzles: Sequence[VerifiedPuzzle], layout: Layout, paper: Paper) -> Scene:
    columns, rows = (1, 2) if layout == "2up" else (2, 2)
    capacity = columns * rows
    if not puzzles or len(puzzles) > capacity:
        raise ValueError(f"{layout} requires between 1 and {capacity} puzzles")

    page_width, page_height = PAPER_SIZES[paper]
    margin = 36_000
    gutter = 18_000
    header_bottom = 105_000
    slot_width = (page_width - 2 * margin - (columns - 1) * gutter) // columns
    slot_height = (page_height - header_bottom - margin - (rows - 1) * gutter) // rows
    page = Scene(page_width, page_height)
    page.operations.append(FillRect(0, 0, page_width, page_height, WHITE))

    add_centered_friendly_title(
        page,
        "KenKen Puzzles",
        page_width // 2,
        37_000,
        25_000,
        INK,
        stroke_width=2_600,
    )
    add_centered_proportional_text(
        page,
        _INSTRUCTION[0],
        page_width // 2,
        68_000,
        8_000,
        INK,
        stroke_width=750,
    )
    add_centered_proportional_text(
        page,
        _INSTRUCTION[1],
        page_width // 2,
        81_000,
        8_000,
        INK,
        stroke_width=750,
    )

    for index, verified in enumerate(puzzles):
        row, column = divmod(index, columns)
        x = margin + column * (slot_width + gutter)
        y = header_bottom + row * (slot_height + gutter)
        _add_panel(
            page,
            verified,
            index + 1,
            _PANEL_ACCENTS[index % len(_PANEL_ACCENTS)],
            x,
            y,
            slot_width,
            slot_height,
        )
    return page


def _add_panel(
    page: Scene,
    verified: VerifiedPuzzle,
    ordinal: int,
    accent: Color,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    panel_inset = 3_000
    page.operations.append(
        StrokePath(
            (
                (x + panel_inset, y + panel_inset),
                (x + width - panel_inset, y + panel_inset),
                (x + width - panel_inset, y + height - panel_inset),
                (x + panel_inset, y + height - panel_inset),
            ),
            700,
            accent,
            closed=True,
        )
    )

    label = f"Puzzle {ordinal}"
    label_height = 9_500
    label_width = text_width(label, label_height)
    badge_x = x + 9_000
    badge_y = y + 7_000
    page.operations.append(FillRect(badge_x, badge_y, label_width + 12_000, 17_000, accent))
    add_text(
        page,
        label,
        badge_x + 6_000,
        badge_y + 3_300,
        label_height,
        WHITE,
        stroke_width=1_000,
    )

    puzzle = verified.definition
    metadata = f"{puzzle.size} {MULTIPLICATION} {puzzle.size}"
    profile = _profile_label(verified)
    if profile is not None:
        metadata += f"   {profile}"
    metadata_height = 7_000
    available_width = x + width - 9_000 - (badge_x + label_width + 20_000)
    while text_width(metadata, metadata_height) > available_width:
        metadata_height -= 250
    add_text(
        page,
        metadata,
        badge_x + label_width + 20_000,
        badge_y + 5_000,
        metadata_height,
        accent,
        stroke_width=700,
    )

    add_text(
        page,
        puzzle.id,
        x + 9_000,
        y + height - 12_000,
        5_500,
        (101, 110, 123),
        stroke_width=500,
    )
    board = puzzle_scene(verified, style=SHEET_STYLE)
    place_scene(
        board,
        page,
        x + 9_000,
        y + 29_000,
        width - 18_000,
        height - 46_000,
    )


def _profile_label(verified: VerifiedPuzzle) -> str | None:
    provenance = verified.definition.provenance
    if provenance is None or provenance.profile not in {"easy", "medium", "hard"}:
        return None
    return f"Profile: {provenance.profile.title()}"
