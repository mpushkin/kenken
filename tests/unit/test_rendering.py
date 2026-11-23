from dataclasses import replace

from kenken.model import CageV1, CellV1, ProvenanceV1, PuzzleDefinitionV1
from kenken.rendering import (
    compose_page,
    puzzle_scene,
    serialize_pdf,
    serialize_pdf_pages,
    serialize_png,
    serialize_svg,
    standalone_page,
)
from kenken.rendering.page import _profile_label
from kenken.rendering.puzzle import CAGE_FILLS, SHEET_STYLE, _clue_height
from kenken.rendering.scene import FillRect, StrokePath
from kenken.rendering.typography import MULTIPLICATION, text_width
from kenken.serialization import compute_puzzle_id
from kenken.solver import verify


def test_all_backends_are_deterministic_and_have_valid_signatures(
    unique_puzzle: PuzzleDefinitionV1,
) -> None:
    verified, _ = verify(unique_puzzle)
    assert verified is not None
    scene = standalone_page(puzzle_scene(verified))
    svg = serialize_svg(scene)
    png = serialize_png(scene, 300, 300)
    pdf = serialize_pdf(scene)
    assert svg == serialize_svg(scene)
    assert png == serialize_png(scene, 300, 300)
    assert pdf == serialize_pdf(scene)
    assert svg.startswith(b'<?xml version="1.0"')
    assert b"<text" not in svg
    assert b"href=" not in svg
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
    assert pdf.startswith(b"%PDF-1.4")
    assert b"/Font" not in pdf
    assert pdf.endswith(b"%%EOF\n")


def test_multipage_pdf_is_deterministic_and_font_independent(
    unique_puzzle: PuzzleDefinitionV1,
) -> None:
    verified, _ = verify(unique_puzzle)
    assert verified is not None
    page = compose_page([verified] * 4, "4up", "a4")
    pdf = serialize_pdf_pages((page, page))
    assert pdf == serialize_pdf_pages((page, page))
    assert b"/Count 2" in pdf
    assert pdf.count(b"/Type /Page ") == 2
    assert pdf.count(b"/MediaBox [0 0 595.276 841.89]") == 2
    assert b"/Font" not in pdf


def test_solution_layer_and_printable_page_composition(
    unique_puzzle: PuzzleDefinitionV1,
) -> None:
    verified, _ = verify(unique_puzzle)
    assert verified is not None
    unsolved = puzzle_scene(verified)
    solved = puzzle_scene(verified, verified.solution)
    page = compose_page([verified, verified], "2up", "a4")
    assert (page.width, page.height) == (595_276, 841_890)
    assert len(solved.operations) > len(unsolved.operations)
    assert len(page.operations) > len(solved.operations)
    assert isinstance(page.operations[0], FillRect)


def test_sheet_style_uses_deterministic_pale_cage_fills(
    unique_puzzle: PuzzleDefinitionV1,
) -> None:
    verified, _ = verify(unique_puzzle)
    assert verified is not None
    first = puzzle_scene(verified, style=SHEET_STYLE)
    second = puzzle_scene(verified, style=SHEET_STYLE)
    fills = [
        operation.color
        for operation in first.operations
        if isinstance(operation, FillRect) and operation.color in CAGE_FILLS
    ]
    assert fills
    assert first == second
    assert set(fills) <= set(CAGE_FILLS)
    assert any(isinstance(operation, StrokePath) for operation in first.operations)


def test_profile_labels_are_qualified_and_recognized_only(
    unique_puzzle: PuzzleDefinitionV1,
) -> None:
    verified, _ = verify(unique_puzzle)
    assert verified is not None
    assert _profile_label(verified) is None

    def with_profile(profile: str) -> str | None:
        provenance = ProvenanceV1("test", "1", profile, 1)
        definition = replace(verified.definition, provenance=provenance)
        return _profile_label(replace(verified, definition=definition))

    assert with_profile("easy") == "Profile: Easy"
    assert with_profile("medium") == "Profile: Medium"
    assert with_profile("hard") == "Profile: Hard"
    assert with_profile("custom") is None


def test_every_scene_operation_stays_inside_the_canvas(
    unique_puzzle: PuzzleDefinitionV1,
) -> None:
    verified, _ = verify(unique_puzzle)
    assert verified is not None
    scenes = (
        puzzle_scene(verified),
        standalone_page(puzzle_scene(verified, verified.solution)),
        compose_page([verified] * 4, "4up", "letter"),
    )
    for scene in scenes:
        for operation in scene.operations:
            if isinstance(operation, FillRect):
                assert 0 <= operation.x <= operation.x + operation.width <= scene.width
                assert 0 <= operation.y <= operation.y + operation.height <= scene.height
            else:
                assert all(0 <= x <= scene.width for x, _ in operation.points)
                assert all(0 <= y <= scene.height for _, y in operation.points)


def test_nine_by_nine_coordinate_and_clue_geometry_does_not_clip() -> None:
    size = 9
    cages = tuple(
        CageV1(
            target=(row + column) % size + 1,
            operator="given",
            cells=(CellV1(row, column),),
        )
        for row in range(size)
        for column in range(size)
    )
    bare = PuzzleDefinitionV1("kenken.puzzle/v1", "", size, cages)
    puzzle = replace(bare, id=compute_puzzle_id(bare))
    verified, result = verify(puzzle)
    assert verified is not None
    assert result.status == "unique"
    scene = standalone_page(puzzle_scene(verified))
    for operation in scene.operations:
        if isinstance(operation, FillRect):
            assert 0 <= operation.x <= operation.x + operation.width <= scene.width
            assert 0 <= operation.y <= operation.y + operation.height <= scene.height
        else:
            assert all(0 <= x <= scene.width for x, _ in operation.points)
            assert all(0 <= y <= scene.height for _, y in operation.points)


def test_four_digit_multiply_clue_meets_four_up_fit_rule() -> None:
    clue = f"4032{MULTIPLICATION}"
    height = _clue_height(clue)
    assert text_width(clue, height) <= 840
    # A 6x6 board gets at least this scale in the narrower A4 4-up slot.
    assert height * 36_500 // 1_000 >= 7_000
