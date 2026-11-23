# KenKen CLI

Generate a puzzle from a seed, check that it has exactly one solution, and print it as a PDF. The generator builds 4×4, 5×5, or 6×6 boards in three difficulty bands. The renderer can also produce SVG and PNG.

[Print Set 21, a collection of 28 puzzles on seven A4 pages](examples/set-21.pdf).

## Quick start

Use Python 3.12 or newer and [uv](https://docs.astral.sh/uv/). The CLI uses only the Python standard library at runtime.

```sh
git clone https://github.com/mpushkin/kenken.git
cd kenken
uv sync --locked
mkdir -p build
uv run kenken generate --size 4 --seed 42 --profile medium \
  --output build/puzzle.json --solution-output build/solution.json
uv run kenken verify build/puzzle.json
uv run kenken render build/puzzle.json --format pdf --output build/puzzle.pdf
```

Verification prints `kk-4x4-bad023bceac528f2: unique (solutions=1, nodes=3)`. Open `build/puzzle.pdf` to play. Fill each row and column with the numbers 1 through 4 exactly once, using each outlined cage’s target and operation as clues. The answer key stays in `build/solution.json`.

## Print a sheet

Generate another puzzle and put the pair on one A4 page. The sheet command also supports `4up` and US Letter paper.

```sh
uv run kenken generate --size 4 --seed 43 --profile easy --output build/second.json
uv run kenken sheet build/puzzle.json build/second.json \
  --layout 2up --paper a4 --format pdf --output build/sheet.pdf
```

Use `uv run kenken verify build/puzzle.json --json` for machine-readable results. Add `--include-solution` to include the solution grid. Each subcommand lists its options with `--help`.

## Development

```sh
uv run pytest
uv run ruff check .
uv run mypy
```

See [Puzzle format and verification](docs/architecture.md) for the identity and solver contracts. The JSON schemas live in [schemas/](schemas/) and the reference checksums in [tests/fixtures/golden/](tests/fixtures/golden/). The historical collection scripts use earlier volumes to check for duplicate puzzles across releases. The CLI quick start generates and verifies new puzzles independently of that archive.

[MIT License](LICENSE)
