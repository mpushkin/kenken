import hashlib
import json
import shutil
from pathlib import Path

import pytest

from kenken.model import PuzzleDefinitionV1, SolutionV1
from kenken.rendering import compose_page, serialize_pdf, serialize_pdf_pages
from kenken.serialization import parse_puzzle_bytes, serialize_solution_bytes
from kenken.solver import verify

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def unique_puzzle() -> PuzzleDefinitionV1:
    return parse_puzzle_bytes((FIXTURES / "puzzles" / "unique-3x3.json").read_bytes())


@pytest.fixture
def multiple_puzzle() -> PuzzleDefinitionV1:
    return parse_puzzle_bytes((FIXTURES / "puzzles" / "multiple-3x3.json").read_bytes())


@pytest.fixture
def unsatisfiable_puzzle() -> PuzzleDefinitionV1:
    return parse_puzzle_bytes(
        (FIXTURES / "puzzles" / "unsatisfiable-3x3.json").read_bytes()
    )


@pytest.fixture(scope="session")
def collection_project(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Materialize the historical JSON and audited renderings in pytest's private root."""
    fixture_dir = FIXTURES / "collections"
    root = tmp_path_factory.mktemp("collection-project")
    scripts = root / "scripts"
    scripts.mkdir()
    # The builder binds its volume specs to its own checkout when imported.
    builder = Path(__file__).parents[1] / "scripts" / "build_collection.py"
    shutil.copyfile(builder, scripts / builder.name)
    puzzles = {
        json.loads(line)["id"]: line
        for line in (fixture_dir / "puzzles.jsonl").read_bytes().splitlines(keepends=True)
    }
    reports = {
        row["puzzle_id"]: row["report"]
        for row in map(json.loads, (fixture_dir / "reports.jsonl").read_text().splitlines())
    }
    pdf_root = root / "output" / "pdf"
    for line in (fixture_dir / "manifests.jsonl").read_bytes().splitlines(keepends=True):
        manifest = json.loads(line)
        volume = manifest.get("volume", 1)
        package = pdf_root if volume == 1 else pdf_root / f"volume-{volume}"
        (package / "sources").mkdir(parents=True)
        (package / "collection-manifest.json").write_bytes(line)
        scenes = []
        for page in manifest["pages"]:
            verified_page = []
            for item in page["puzzles"]:
                puzzle_id = item["puzzle_id"]
                path = package / item["puzzle_file"]
                path.write_bytes(puzzles[puzzle_id])
                if puzzle_id in reports:
                    data = json.dumps(reports[puzzle_id], sort_keys=True, separators=(",", ":"))
                    stem = path.name.removesuffix(".puzzle.json")
                    path.with_name(stem + ".report.json").write_text(data + "\n")
                if volume == 4:
                    puzzle = parse_puzzle_bytes(puzzles[puzzle_id])
                    checked, result = verify(puzzle)
                    assert checked is not None and result.status == "unique"
                    verified_page.append(checked)
                    solution = SolutionV1("kenken.solution/v1", puzzle.id, checked.solution)
                    solution_path = package / item["solution_file"]
                    solution_path.write_bytes(serialize_solution_bytes(solution, puzzle))
            if volume == 4:
                scene = compose_page(verified_page, "4up", "a4")
                scenes.append(scene)
                (package / page["page_pdf"]).write_bytes(serialize_pdf(scene))
        if volume == 4:
            (package / manifest["collection_pdf"]).write_bytes(serialize_pdf_pages(scenes))
            for relative, expected in manifest["artifact_sha256"].items():
                actual = hashlib.sha256((package / relative).read_bytes()).hexdigest()
                assert actual == expected, relative
    return root
