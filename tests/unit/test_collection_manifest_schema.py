from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import ValidationError
from jsonschema.validators import Draft202012Validator

ROOT = Path(__file__).parents[2]
SCHEMA = json.loads(
    (ROOT / "schemas" / "kenken-collection-manifest-v3.schema.json").read_text()
)
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)


def _puzzle(ordinal: int, seed: int) -> dict[str, object]:
    stem = f"sources/page-01-4x4-easy-puzzle-{ordinal:02d}-seed-{seed}"
    return {
        "accepted_attempt": ordinal,
        "given_cages": 2,
        "ordinal": ordinal,
        "puzzle_file": f"{stem}.puzzle.json",
        "puzzle_id": f"kk-4x4-{ordinal:016x}",
        "report_file": f"{stem}.report.json",
        "seed": str(seed),
        "solution_file": f"{stem}.solution.json",
    }


def _manifest() -> dict[str, object]:
    pages = []
    signature = (
        (1, 4, "easy"),
        (2, 4, "easy"),
        (3, 4, "medium"),
        (4, 4, "hard"),
        (5, 5, "easy"),
        (6, 5, "medium"),
        (7, 5, "hard"),
    )
    for number, size, profile in signature:
        records = [_puzzle(ordinal, 2026072800 + ordinal) for ordinal in range(1, 5)]
        for ordinal, record in enumerate(records, start=1):
            record["puzzle_id"] = f"kk-{size}x{size}-{number * 10 + ordinal:016x}"
        pages.append(
            {
                "page_number": number,
                "page_pdf": f"kenken-page-{number:02d}-{size}x{size}-{profile}-a4.pdf",
                "profile": profile,
                "puzzles": records,
                "size": size,
            }
        )
    return {
        "artifact_sha256": {
            "../kenken-28-puzzle-collection-a4-volume-4.pdf": "a" * 64
        },
        "collection_pdf": "../kenken-28-puzzle-collection-a4-volume-4.pdf",
        "cross_volume": {
            "distinct_from_priors": True,
            "prior_collections": [
                {
                    "manifest": "../collection-manifest.json",
                    "puzzle_count": 24,
                    "volume": 1,
                }
            ],
            "prior_puzzle_count": 24,
        },
        "generation": {
            "arithmetic_cage_policy": {
                "applies_to_profiles": ["easy"],
                "limits": {
                    "max_add_target": 18,
                    "max_add_terms": 3,
                    "max_cage_cells": 3,
                    "max_multiply_factors": 2,
                    "max_multiply_target": 36,
                },
                "policy": "arithmetic-cap-v1",
            },
            "given_cage_policy": {
                "max_by_profile": {"easy": 4, "hard": 1, "medium": 2},
                "policy": "given-cap-v1",
            },
            "max_attempts_per_puzzle": 2000,
            "max_solver_nodes": 1_000_000,
            "seed_namespace": "20260728xx",
        },
        "page_geometry_points": {"height": "841.89", "width": "595.276"},
        "pages": pages,
        "schema": "kenken.collection-manifest/v3",
        "volume": 4,
    }


def test_v3_schema_accepts_two_ordered_easy_pages() -> None:
    manifest = _manifest()

    VALIDATOR.validate(manifest)
    assert [
        (page["page_number"], page["size"], page["profile"])
        for page in manifest["pages"]
    ][:2] == [(1, 4, "easy"), (2, 4, "easy")]


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value.update({"unexpected": True}),
        lambda value: value["pages"][0].update({"unexpected": True}),
        lambda value: value["pages"][0]["puzzles"][0].update({"unexpected": True}),
        lambda value: value["pages"][0].update(
            {"puzzles": value["pages"][0]["puzzles"][:3]}
        ),
    ],
)
def test_v3_schema_rejects_unknown_fields_and_non_four_up_pages(mutate: object) -> None:
    manifest = copy.deepcopy(_manifest())
    mutate(manifest)  # type: ignore[operator]

    with pytest.raises(ValidationError):
        VALIDATOR.validate(manifest)
