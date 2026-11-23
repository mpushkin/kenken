# Historical collection fixtures

These three JSON Lines files exercise compatibility with published collection formats. Each line is one JSON record.

- `puzzles.jsonl` contains the 520 canonical puzzle definitions in Volumes 1–19. The Volume 20 prior-chain check recalculates each ID from its cages.
- `manifests.jsonl` contains the schema, identity, relative paths, and recorded prior counts used to read those 19 volumes. Volume 4 retains its complete manifest and original 92 SHA-256 values.
- `reports.jsonl` pairs puzzle IDs with their original generation reports. It contains the Volume 2 v2 arithmetic-policy example and all 28 v3 reports from Volume 4. Different puzzles can share a seed.

Pytest builds the historical directory layout in a temporary directory. It solves the 28 Volume 4 puzzles, serializes their solution sidecars, renders the seven pages and the combined PDF, and checks all 92 files against the original manifest. The audit tests change one report and update its manifest hash before exercising the independent semantic check.

