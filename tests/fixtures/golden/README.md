# Artifact golden reference

`artifact-sha256.json` fixes the exact bytes for a generated medium 4×4 puzzle
from seed 42, its generation report, unsolved standalone SVG/PNG/PDF output, a
solved standalone SVG, an A4 2-up PDF sheet, and a Letter 4-up PDF sheet.

The reference was recorded with:

- Python 3.13.13
- macOS 26.5.1 arm64
- the committed `uv.lock`
- the bundled KenKen vector stroke face

Python 3.12 or newer under the committed lockfile is the supported environment.
The serializers use only specified integer operations and explicit byte
encodings. PNG uses stored DEFLATE blocks, so its bytes do not depend on the
host zlib compression strategy. Every supported environment is expected to
match these hashes; a deliberate format change must update the format contract,
goldens, and this record together.

The puzzle JSON and generation-report hashes are intentionally unchanged by
the visual upgrade. Every render hash changed because ordered RGB paint
operations, coordinate gutters, vector operator glyphs, line hierarchy,
solution styling, and editorial sheet composition are now part of the
deterministic rendering contract.

The later sheet-header refinement changed only the A4 2-up and Letter 4-up
PDF hashes. It adds a fixed friendly display run, proportional header spacing,
and clearer fixed rule copy; standalone board and canonical JSON hashes remain
unchanged.

Generator v0.2 intentionally changes the puzzle JSON and generation-report
hashes in this fixture. The representative medium seed retains the same cage
identity and therefore the same render bytes, but puzzle provenance advances
to `0.2.0` and the report advances to `kenken.generation-report/v2`. Other
size/profile/seed combinations may resolve to different cages under the
`given-cap-v1` policy, which limits the number of given cages by difficulty.

Generator v0.3 advances the same representative puzzle's provenance and moves
the report writer to `kenken.generation-report/v3`. Its medium cage identity
and every render byte remain unchanged because `arithmetic-cap-v1` is
non-applicable outside easy generation. The report now records accepted
arithmetic maxima as observations. Easy generation additionally uses a
three-cell cap. Multiplication allows two factors and a target up to 36.
Addition allows three terms and a target up to 18.
