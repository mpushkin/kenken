# Puzzle format and verification

A puzzle file contains the clues a player sees. A solution file carries a grid
and the ID of the puzzle it solves. Generation, verification, and rendering all
use the same reader and cage arithmetic. The schemas describe their JSON
shapes. [Puzzle schema](../schemas/kenken-puzzle-v1.schema.json) ·
[Solution schema](../schemas/kenken-solution-v1.schema.json).

## Puzzle format

A `kenken.puzzle/v1` board has size 3 through 9. Coordinates are zero-based.
Cages cover every cell exactly once and each cage is orthogonally connected.
Every target is a positive integer. For a board of size N and a cage of k
cells, these rules apply.

| Operator | Cells | Target | Upper bound |
| --- | --- | --- | --- |
| `given` | 1 | Cell value | N |
| `add` | 2–4 | Sum | k × N |
| `multiply` | 2–4 | Product | N to the power k |
| `subtract` | 2 | Absolute difference | N − 1 |
| `divide` | 2 | Exact quotient of the larger by the smaller | N |

The reader rejects duplicate keys, unknown fields, invalid scalar types, and
cages with no possible assignment consistent with row and column constraints.
A supplied ID must match the one computed from the clues.

## Identity

Cells within each cage are sorted by row and then column. Cages are sorted by
their first cell. The identity contains exactly three fields, `schema`, `size`,
and the normalized `cages`. The writer sorts JSON keys, uses compact separators,
encodes UTF-8 without a byte-order mark, and appends one LF. SHA-256 of those
bytes gives the ID in the form `kk-{size}x{size}-{first 16 hex digits}`.
Changing provenance or reordering input cages leaves the ID unchanged. The
[3×3 example](../tests/fixtures/puzzles/unique-3x3.json) has ID
`kk-3x3-748280b20a5aba7e`.

## Solutions and verification

A `kenken.solution/v1` sidecar carries a matching `puzzle_id` and an N × N
integer grid. Its rows and columns must each contain every integer from 1 to N
exactly once, and each cage must satisfy its clue.

The solver propagates constraints to a fixed point and branches on the cell
with the fewest remaining values, breaking ties in row-major order. It tries
values in ascending order and stops after the second solution. Each search
has a positive node budget, which defaults to 1,000,000 and counts the root as
node one. A complete search reports `unsatisfiable`, `unique`, or `multiple`.
If the budget runs out before the result is established, it reports `unknown`.

## Generation and rendering

The generator supports sizes 4, 5, and 6. It uses a seeded SplitMix64 stream
to build a Latin square and propose cages. Each accepted puzzle passes a
uniqueness proof and a separate solve-one traversal that grades its difficulty.
The generation report records the parameters and rejection counts. The
[report schema](../schemas/kenken-generation-report-v3.schema.json) describes
the current format.

Rendering verifies uniqueness for each input. The SVG, PNG, and PDF backends
share integer scene geometry and bundled vector glyphs. The
[golden fixtures](../tests/fixtures/golden/) record the expected bytes for a
representative generated puzzle, report, and rendered outputs.
