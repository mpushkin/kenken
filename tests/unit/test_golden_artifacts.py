import hashlib
import json
from pathlib import Path

from kenken.generation import (
    GenerationConfig,
    count_given_cages,
    generate,
    given_cage_cap,
    serialize_generation_report,
)
from kenken.rendering import (
    compose_page,
    puzzle_scene,
    serialize_pdf,
    serialize_png,
    serialize_svg,
    standalone_page,
)
from kenken.serialization import serialize_puzzle_bytes
from kenken.solver import verify

GOLDEN = Path(__file__).parents[1] / "fixtures" / "golden" / "artifact-sha256.json"


def test_generation_and_rendering_artifact_hashes() -> None:
    expected = json.loads(GOLDEN.read_text())
    generated = generate(GenerationConfig(4, 42, "medium"))
    assert count_given_cages(generated.puzzle.cages) <= given_cage_cap(4, "medium")
    verified, result = verify(generated.puzzle)
    assert verified is not None
    assert result.status == "unique"
    puzzle = puzzle_scene(verified)
    standalone = standalone_page(puzzle)
    solved = standalone_page(puzzle_scene(verified, verified.solution))
    sheet = compose_page([verified, verified], "2up", "a4")
    four_up = compose_page([verified] * 4, "4up", "letter")
    artifacts = {
        "puzzle-json": serialize_puzzle_bytes(generated.puzzle),
        "generation-report-json": serialize_generation_report(generated.report),
        "standalone-svg": serialize_svg(standalone),
        "standalone-png-300x300": serialize_png(standalone, 300, 300),
        "standalone-pdf": serialize_pdf(standalone),
        "standalone-solved-svg": serialize_svg(solved),
        "a4-2up-pdf": serialize_pdf(sheet),
        "letter-4up-pdf": serialize_pdf(four_up),
    }
    actual = {
        name: hashlib.sha256(data).hexdigest() for name, data in artifacts.items()
    }
    assert actual == expected["hashes"]
