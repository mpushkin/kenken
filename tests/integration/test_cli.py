import json
from pathlib import Path

import pytest

from kenken.cli import _atomic_write_many, main
from kenken.generation import count_given_cages, given_cage_cap
from kenken.model import CageV1, CellV1
from kenken.serialization import parse_puzzle_bytes

FIXTURES = Path(__file__).parents[1] / "fixtures" / "puzzles"


def test_json_verify_and_optional_solution(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(
        [
            "verify",
            str(FIXTURES / "unique-3x3.json"),
            "--json",
            "--include-solution",
        ]
    )
    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert exit_code == 0
    assert output["schema"] == "kenken.verify/v1"
    assert output["status"] == "unique"
    assert output["solution"] == [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
    assert "unique" in captured.err


@pytest.mark.parametrize(
    ("name", "limit", "status"),
    [
        ("multiple-3x3.json", None, "multiple"),
        ("unsatisfiable-3x3.json", None, "unsatisfiable"),
        ("multiple-3x3.json", "1", "unknown"),
    ],
)
def test_non_unique_statuses_exit_three(
    capsys: pytest.CaptureFixture[str], name: str, limit: str | None, status: str
) -> None:
    args = ["verify", str(FIXTURES / name), "--json"]
    if limit is not None:
        args.extend(["--max-solver-nodes", limit])
    assert main(args) == 3
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == status
    assert "solution" not in output


def test_structural_error_exits_two(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    puzzle = tmp_path / "bad.json"
    puzzle.write_text('{"schema":"kenken.puzzle/v1"}')
    assert main(["verify", str(puzzle)]) == 2
    assert "missing field" in capsys.readouterr().err


@pytest.mark.parametrize("limit", ["0", "-1", "nope"])
def test_invalid_limit_is_usage_error(limit: str) -> None:
    with pytest.raises(SystemExit) as error:
        main(
            [
                "verify",
                str(FIXTURES / "unique-3x3.json"),
                "--max-solver-nodes",
                limit,
            ]
        )
    assert error.value.code == 2


def test_include_solution_requires_json() -> None:
    with pytest.raises(SystemExit) as error:
        main(
            [
                "verify",
                str(FIXTURES / "unique-3x3.json"),
                "--include-solution",
            ]
        )
    assert error.value.code == 2


def test_generate_verify_and_render_all_formats(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    puzzle = tmp_path / "generated.json"
    solution = tmp_path / "solution.json"
    report = tmp_path / "report.json"
    assert (
        main(
            [
                "generate",
                "--size",
                "4",
                "--seed",
                "42",
                "--profile",
                "medium",
                "--output",
                str(puzzle),
                "--solution-output",
                str(solution),
                "--report-output",
                str(report),
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert main(["verify", str(puzzle), "--json"]) == 0
    capsys.readouterr()
    generated_puzzle = parse_puzzle_bytes(puzzle.read_bytes())
    assert count_given_cages(generated_puzzle.cages) <= given_cage_cap(4, "medium")
    assert json.loads(report.read_text())["evaluated_difficulty"]["band"] == "medium"

    for output_format, signature in (
        ("svg", b"<?xml"),
        ("png", b"\x89PNG"),
        ("pdf", b"%PDF"),
    ):
        output = tmp_path / f"puzzle.{output_format}"
        assert (
            main(
                [
                    "render",
                    str(puzzle),
                    "--format",
                    output_format,
                    "--output",
                    str(output),
                    "--solution",
                    str(solution),
                    "--dpi",
                    "72",
                ]
            )
            == 0
        )
        assert output.read_bytes().startswith(signature)
        capsys.readouterr()


def test_render_and_sheet_failures_do_not_create_or_replace_output(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "protected.svg"
    output.write_bytes(b"existing")
    multiple = FIXTURES / "multiple-3x3.json"
    unique = FIXTURES / "unique-3x3.json"

    assert (
        main(
            [
                "render",
                str(multiple),
                "--format",
                "svg",
                "--output",
                str(output),
                "--max-solver-nodes",
                "1",
            ]
        )
        == 3
    )
    assert output.read_bytes() == b"existing"
    assert "verification is unknown" in capsys.readouterr().err

    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"schema":"kenken.puzzle/v1"}')
    assert (
        main(
            [
                "render",
                str(invalid),
                "--format",
                "svg",
                "--output",
                str(output),
            ]
        )
        == 2
    )
    assert output.read_bytes() == b"existing"
    capsys.readouterr()

    assert (
        main(
            [
                "sheet",
                str(unique),
                str(multiple),
                "--layout",
                "2up",
                "--paper",
                "letter",
                "--format",
                "svg",
                "--output",
                str(output),
            ]
        )
        == 3
    )
    assert output.read_bytes() == b"existing"
    capsys.readouterr()

    assert (
        main(
            [
                "render",
                str(FIXTURES / "unsatisfiable-3x3.json"),
                "--format",
                "svg",
                "--output",
                str(output),
            ]
        )
        == 3
    )
    assert output.read_bytes() == b"existing"
    assert "verification is unsatisfiable" in capsys.readouterr().err


def test_sheet_renders_a4_and_letter_layouts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    puzzle = FIXTURES / "unique-3x3.json"
    for layout, paper, output_format in (
        ("2up", "a4", "svg"),
        ("4up", "letter", "pdf"),
    ):
        output = tmp_path / f"{layout}-{paper}.{output_format}"
        args = [
            "sheet",
            str(puzzle),
            str(puzzle),
            "--layout",
            layout,
            "--paper",
            paper,
            "--format",
            output_format,
            "--output",
            str(output),
        ]
        assert main(args) == 0
        assert output.stat().st_size > 100
        capsys.readouterr()


def test_generation_rejects_invalid_later_destination_before_replacing_primary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    puzzle = tmp_path / "puzzle.json"
    puzzle.write_bytes(b"original puzzle")
    solution_directory = tmp_path / "solution"
    solution_directory.mkdir()
    report = tmp_path / "report.json"
    assert (
        main(
            [
                "generate",
                "--size",
                "4",
                "--seed",
                "42",
                "--profile",
                "easy",
                "--output",
                str(puzzle),
                "--solution-output",
                str(solution_directory),
                "--report-output",
                str(report),
            ]
        )
        == 5
    )
    assert puzzle.read_bytes() == b"original puzzle"
    assert solution_directory.is_dir()
    assert not report.exists()
    assert "not a regular file" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("solution_name", "report_name"),
    [
        ("puzzle.json", "report.json"),
        ("solution.json", "puzzle.json"),
        ("shared.json", "shared.json"),
    ],
)
def test_generation_rejects_every_duplicate_destination_combination(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    solution_name: str,
    report_name: str,
) -> None:
    puzzle = tmp_path / "puzzle.json"
    solution = tmp_path / solution_name
    report = tmp_path / report_name
    touched = {puzzle, solution, report}
    for path in touched:
        path.write_bytes(f"existing:{path.name}".encode())
    before = {path: path.read_bytes() for path in touched}
    assert (
        main(
            [
                "generate",
                "--size",
                "4",
                "--seed",
                "42",
                "--profile",
                "easy",
                "--output",
                str(puzzle),
                "--solution-output",
                str(solution),
                "--report-output",
                str(report),
            ]
        )
        == 5
    )
    assert {path: path.read_bytes() for path in touched} == before
    assert "must be distinct" in capsys.readouterr().err


def test_exhaustion_with_colliding_report_path_preserves_existing_puzzle(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    puzzle = tmp_path / "puzzle.json"
    puzzle.write_bytes(b"existing puzzle")
    assert (
        main(
            [
                "generate",
                "--size",
                "4",
                "--seed",
                "42",
                "--profile",
                "hard",
                "--max-attempts",
                "1",
                "--output",
                str(puzzle),
                "--report-output",
                str(puzzle),
            ]
        )
        == 5
    )
    assert puzzle.read_bytes() == b"existing puzzle"
    assert "must be distinct" in capsys.readouterr().err


def test_cap_driven_exhaustion_writes_only_v3_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    puzzle = tmp_path / "puzzle.json"
    solution = tmp_path / "solution.json"
    report = tmp_path / "report.json"

    def all_givens(grid: tuple[tuple[int, ...], ...], *args: object) -> tuple[CageV1, ...]:
        return tuple(
            CageV1(grid[row][column], "given", (CellV1(row, column),))
            for row in range(4)
            for column in range(4)
        )

    monkeypatch.setattr("kenken.generation.generator.build_cages", all_givens)
    assert (
        main(
            [
                "generate",
                "--size",
                "4",
                "--seed",
                "42",
                "--profile",
                "easy",
                "--max-attempts",
                "1",
                "--output",
                str(puzzle),
                "--solution-output",
                str(solution),
                "--report-output",
                str(report),
            ]
        )
        == 4
    )
    assert not puzzle.exists()
    assert not solution.exists()
    payload = json.loads(report.read_text())
    assert report.read_bytes().endswith(b"\n")
    assert payload["schema"] == "kenken.generation-report/v3"
    assert payload["given_cage_policy"]["accepted_given_cages"] is None
    assert payload["arithmetic_cage_policy"]["accepted_maxima"] is None
    assert payload["rejection_counts"]["given_limit_exceeded"] == 1
    assert sum(payload["rejection_counts"].values()) == payload["attempts"]
    assert "generation exhausted after 1 attempts" in capsys.readouterr().err


def test_transaction_rolls_back_published_and_new_outputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    primary = tmp_path / "primary.json"
    secondary = tmp_path / "secondary.json"
    primary.write_bytes(b"original")
    real_replace = __import__("os").replace
    calls = 0

    def fail_second_publication(source: Path | str, destination: Path | str) -> None:
        nonlocal calls
        calls += 1
        if calls == 3:
            raise OSError("injected publication failure")
        real_replace(source, destination)

    monkeypatch.setattr("kenken.cli.os.replace", fail_second_publication)
    with pytest.raises(OSError, match="injected"):
        _atomic_write_many([(primary, b"new primary"), (secondary, b"new secondary")])
    assert primary.read_bytes() == b"original"
    assert not secondary.exists()
    assert not tuple(tmp_path.glob(".*.tmp"))
    assert not tuple(tmp_path.glob(".*.backup"))
