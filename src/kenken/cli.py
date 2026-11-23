"""Command-line orchestration for generation, verification, and rendering."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn

from kenken.generation import (
    GenerationConfig,
    GenerationExhausted,
    generate,
    serialize_generation_report,
)
from kenken.model import SolutionV1, SolveResult, VerifiedPuzzle
from kenken.rendering import (
    compose_page,
    puzzle_scene,
    serialize_pdf,
    serialize_png,
    serialize_svg,
    standalone_page,
)
from kenken.rendering.page import PAPER_SIZES, Layout, Paper
from kenken.serialization import (
    parse_puzzle_bytes,
    parse_solution_bytes,
    serialize_puzzle_bytes,
    serialize_solution_bytes,
)
from kenken.solver import verify
from kenken.validation import ValidationError


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n")


def _positive_integer(value: str) -> int:
    try:
        parsed = int(value, 10)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a positive integer") from error
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _uint64(value: str) -> int:
    try:
        parsed = int(value, 10)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a decimal uint64") from error
    if not 0 <= parsed <= 2**64 - 1:
        raise argparse.ArgumentTypeError("must be a decimal uint64")
    return parsed


def _add_budget(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--max-solver-nodes",
        type=_positive_integer,
        default=1_000_000,
        metavar="POSITIVE_INT",
    )


def _parser() -> _ArgumentParser:
    parser = _ArgumentParser(prog="kenken")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="generate a verified puzzle")
    generate_parser.add_argument("--size", required=True, type=int, choices=(4, 5, 6))
    generate_parser.add_argument("--seed", required=True, type=_uint64)
    generate_parser.add_argument("--profile", required=True, choices=("easy", "medium", "hard"))
    generate_parser.add_argument("--output", required=True, type=Path, metavar="PUZZLE.json")
    generate_parser.add_argument("--solution-output", type=Path, metavar="SOLUTION.json")
    generate_parser.add_argument("--report-output", type=Path, metavar="REPORT.json")
    generate_parser.add_argument("--max-attempts", type=_positive_integer, default=1_000)
    _add_budget(generate_parser)

    verify_parser = subparsers.add_parser("verify", help="validate and prove puzzle uniqueness")
    verify_parser.add_argument("puzzle", type=Path, metavar="PUZZLE.json")
    verify_parser.add_argument("--json", action="store_true", dest="json_output")
    verify_parser.add_argument("--include-solution", action="store_true")
    _add_budget(verify_parser)

    render_parser = subparsers.add_parser("render", help="render one verified puzzle")
    render_parser.add_argument("puzzle", type=Path, metavar="PUZZLE.json")
    render_parser.add_argument("--format", required=True, choices=("svg", "png", "pdf"))
    render_parser.add_argument("--output", required=True, type=Path)
    render_parser.add_argument("--dpi", type=_positive_integer, default=300)
    render_parser.add_argument("--solution", type=Path, metavar="SOLUTION.json")
    _add_budget(render_parser)

    sheet_parser = subparsers.add_parser("sheet", help="compose verified puzzles on one page")
    sheet_parser.add_argument("puzzles", nargs="+", type=Path, metavar="PUZZLE.json")
    sheet_parser.add_argument("--layout", required=True, choices=("2up", "4up"))
    sheet_parser.add_argument("--paper", required=True, choices=("a4", "letter"))
    sheet_parser.add_argument("--format", required=True, choices=("svg", "png", "pdf"))
    sheet_parser.add_argument("--output", required=True, type=Path)
    sheet_parser.add_argument("--dpi", type=_positive_integer, default=300)
    _add_budget(sheet_parser)
    return parser


def _stats(result: SolveResult) -> dict[str, int]:
    return {
        "visited_nodes": result.stats.visited_nodes,
        "backtracks": result.stats.backtracks,
        "max_decision_depth": result.stats.max_decision_depth,
        "propagation_rounds": result.stats.propagation_rounds,
    }


def _validate_destinations(destinations: Sequence[Path]) -> None:
    resolved = [path.resolve() for path in destinations]
    if len(resolved) != len(set(resolved)):
        raise ValueError("output paths must be distinct")
    for path in destinations:
        if not path.parent.is_dir():
            raise ValueError(f"output parent is not a directory: {path.parent}")
        if (path.exists() or path.is_symlink()) and not path.is_file():
            raise ValueError(f"output destination is not a regular file: {path}")


def _atomic_write_many(outputs: list[tuple[Path, bytes]]) -> None:
    destinations = [path for path, _ in outputs]
    _validate_destinations(destinations)
    temporary: list[tuple[Path, Path]] = []
    backups: list[tuple[Path, Path]] = []
    published: list[Path] = []
    preserve_backups = False
    rollback_error: OSError | None = None
    try:
        for path, data in outputs:
            descriptor, name = tempfile.mkstemp(
                dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
            )
            temporary_path = Path(name)
            temporary.append((temporary_path, path))
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        for destination in destinations:
            if destination.exists():
                descriptor, name = tempfile.mkstemp(
                    dir=destination.parent,
                    prefix=f".{destination.name}.",
                    suffix=".backup",
                )
                os.close(descriptor)
                backup = Path(name)
                backup.unlink()
                os.replace(destination, backup)
                backups.append((backup, destination))
        for temporary_path, destination in temporary:
            os.replace(temporary_path, destination)
            published.append(destination)
    except BaseException as error:
        for destination in reversed(published):
            try:
                destination.unlink(missing_ok=True)
            except OSError as cleanup_error:
                rollback_error = rollback_error or cleanup_error
        for backup, destination in reversed(backups):
            try:
                os.replace(backup, destination)
            except OSError as restore_error:
                rollback_error = rollback_error or restore_error
        if rollback_error is not None:
            preserve_backups = True
            raise OSError(
                f"output publication failed and rollback was incomplete: {rollback_error}"
            ) from error
        raise
    finally:
        for temporary_path, _ in temporary:
            temporary_path.unlink(missing_ok=True)
        if not preserve_backups:
            for backup, _ in backups:
                backup.unlink(missing_ok=True)


def _generation_destinations(args: argparse.Namespace) -> list[Path]:
    destinations = [args.output]
    if args.solution_output is not None:
        destinations.append(args.solution_output)
    if args.report_output is not None:
        destinations.append(args.report_output)
    return destinations


def _validate_generation_destinations(args: argparse.Namespace) -> bool:
    try:
        _validate_destinations(_generation_destinations(args))
    except (OSError, ValueError) as error:
        print(f"kenken generate: {error}", file=sys.stderr)
        return False
    return True


def _run_generate(args: argparse.Namespace) -> int:
    if not _validate_generation_destinations(args):
        return 5
    config = GenerationConfig(
        size=args.size,
        seed=args.seed,
        profile=args.profile,
        max_attempts=args.max_attempts,
        max_solver_nodes=args.max_solver_nodes,
    )
    try:
        generated = generate(config)
    except GenerationExhausted as error:
        if args.report_output is not None:
            try:
                _atomic_write_many(
                    [(args.report_output, serialize_generation_report(error.report))]
                )
            except (OSError, ValueError) as write_error:
                print(f"kenken generate: {write_error}", file=sys.stderr)
                return 5
        print(str(error), file=sys.stderr)
        return 4

    solution = SolutionV1("kenken.solution/v1", generated.puzzle.id, generated.solution)
    outputs = [(args.output, serialize_puzzle_bytes(generated.puzzle))]
    if args.solution_output is not None:
        outputs.append(
            (
                args.solution_output,
                serialize_solution_bytes(solution, generated.puzzle),
            )
        )
    if args.report_output is not None:
        outputs.append((args.report_output, serialize_generation_report(generated.report)))
    try:
        _atomic_write_many(outputs)
    except (OSError, ValueError) as error:
        print(f"kenken generate: {error}", file=sys.stderr)
        return 5
    print(
        f"{generated.puzzle.id}: generated {generated.difficulty.band} "
        f"at attempt {generated.report.accepted_attempt}"
    )
    return 0


def _run_verify(args: argparse.Namespace) -> int:
    if args.include_solution and not args.json_output:
        _parser().error("--include-solution requires --json")
    try:
        puzzle = parse_puzzle_bytes(args.puzzle.read_bytes())
        verified, result = verify(puzzle, args.max_solver_nodes)
    except (OSError, ValidationError, ValueError) as error:
        print(f"kenken verify: {error}", file=sys.stderr)
        return 2

    if args.json_output:
        output: dict[str, object] = {
            "schema": "kenken.verify/v1",
            "puzzle_id": puzzle.id,
            "status": result.status,
            "solutions_found": result.solutions_found,
            "stats": _stats(result),
        }
        if args.include_solution and verified is not None:
            output["solution"] = [list(row) for row in verified.solution]
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
        print(f"{puzzle.id}: {result.status}", file=sys.stderr)
    else:
        print(
            f"{puzzle.id}: {result.status} "
            f"(solutions={result.solutions_found}, nodes={result.stats.visited_nodes})"
        )
    return 0 if result.status == "unique" else 3


def _verified_input(
    path: Path, max_solver_nodes: int
) -> tuple[VerifiedPuzzle | None, SolveResult | None, str | None]:
    try:
        puzzle = parse_puzzle_bytes(path.read_bytes())
        verified, result = verify(puzzle, max_solver_nodes)
    except (OSError, ValidationError, ValueError) as error:
        return None, None, str(error)
    return verified, result, None


def _serialized_scene(
    scene: object, output_format: str, dpi: int, *, paper: Paper | None = None
) -> bytes:
    from kenken.rendering.scene import Scene

    if not isinstance(scene, Scene):
        raise TypeError("expected a rendering scene")
    if output_format == "svg":
        return serialize_svg(scene)
    if output_format == "pdf":
        return serialize_pdf(scene)
    if paper is None:
        width = height = 6 * dpi
    else:
        page_width, page_height = PAPER_SIZES[paper]
        width = max(1, page_width * dpi // 72_000)
        height = max(1, page_height * dpi // 72_000)
    return serialize_png(scene, width, height)


def _run_render(args: argparse.Namespace) -> int:
    verified, result, error = _verified_input(args.puzzle, args.max_solver_nodes)
    if error is not None:
        print(f"kenken render: {error}", file=sys.stderr)
        return 2
    if verified is None:
        assert result is not None
        print(f"kenken render: verification is {result.status}", file=sys.stderr)
        return 3
    solution = None
    if args.solution is not None:
        try:
            solution = parse_solution_bytes(args.solution.read_bytes(), verified.definition).grid
        except (OSError, ValidationError) as solution_error:
            print(f"kenken render: {solution_error}", file=sys.stderr)
            return 2
    try:
        scene = standalone_page(puzzle_scene(verified, solution))
        data = _serialized_scene(scene, args.format, args.dpi)
        _atomic_write_many([(args.output, data)])
    except (OSError, ValueError) as render_error:
        print(f"kenken render: {render_error}", file=sys.stderr)
        return 5
    print(f"{verified.definition.id}: rendered {args.format}")
    return 0


def _run_sheet(args: argparse.Namespace) -> int:
    capacity = 2 if args.layout == "2up" else 4
    if len(args.puzzles) > capacity:
        print(
            f"kenken sheet: {args.layout} accepts at most {capacity} puzzles",
            file=sys.stderr,
        )
        return 2
    verified_puzzles: list[VerifiedPuzzle] = []
    for path in args.puzzles:
        verified, result, error = _verified_input(path, args.max_solver_nodes)
        if error is not None:
            print(f"kenken sheet: {path}: {error}", file=sys.stderr)
            return 2
        if verified is None:
            assert result is not None
            print(
                f"kenken sheet: {path}: verification is {result.status}",
                file=sys.stderr,
            )
            return 3
        verified_puzzles.append(verified)
    try:
        layout: Layout = args.layout
        paper: Paper = args.paper
        scene = compose_page(verified_puzzles, layout, paper)
        data = _serialized_scene(scene, args.format, args.dpi, paper=paper)
        _atomic_write_many([(args.output, data)])
    except (OSError, ValueError) as render_error:
        print(f"kenken sheet: {render_error}", file=sys.stderr)
        return 5
    print(f"rendered {len(verified_puzzles)} puzzles as {args.layout} {args.paper}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "generate":
        return _run_generate(args)
    if args.command == "verify":
        return _run_verify(args)
    if args.command == "render":
        return _run_render(args)
    if args.command == "sheet":
        return _run_sheet(args)
    raise AssertionError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
