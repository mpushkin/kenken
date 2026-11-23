import json

import pytest

from kenken.generation import (
    ARITHMETIC_CAGE_POLICY,
    GIVEN_CAGE_POLICY,
    GenerationConfig,
    GenerationExhausted,
    GivenCagePolicyResult,
    classify_difficulty,
    count_given_cages,
    generate,
    given_cage_cap,
    serialize_generation_report,
)
from kenken.model import DifficultyResult, SolveResult, SolveStats, VerifiedPuzzle
from kenken.serialization import parse_puzzle_bytes, serialize_puzzle_bytes
from kenken.solver import solve


@pytest.mark.parametrize(
    ("stats", "expected"),
    [
        (SolveStats(1, 0, 0, 3), "easy"),
        (SolveStats(100, 2, 2, 10), "medium"),
        (SolveStats(101, 2, 2, 10), "hard"),
        (SolveStats(4, 0, 3, 10), "hard"),
    ],
)
def test_search_v1_thresholds(stats: SolveStats, expected: str) -> None:
    assert classify_difficulty(stats) == expected


@pytest.mark.parametrize(
    ("size", "profile", "expected_attempt", "expected_givens"),
    [
        (4, "easy", 1, 4),
        (4, "medium", 23, 1),
        (4, "hard", 541, 0),
        (5, "easy", 2, 4),
        (5, "medium", 91, 1),
        (5, "hard", 549, 1),
        (6, "easy", 19, 3),
        (6, "medium", 173, 2),
        (6, "hard", 10, 0),
    ],
)
def test_generation_is_deterministic_unique_and_matches_requested_profile(
    size: int, profile: str, expected_attempt: int, expected_givens: int
) -> None:
    config = GenerationConfig(size, 42, profile)  # type: ignore[arg-type]
    first = generate(config)
    second = generate(config)
    assert first == second
    assert first.difficulty.band == profile
    assert first.puzzle.provenance is not None
    assert first.puzzle.provenance.profile == profile
    assert first.puzzle.provenance.generator_version == "0.3.0"
    assert first.puzzle.provenance.accepted_attempt == first.report.accepted_attempt
    given_count = count_given_cages(first.puzzle.cages)
    assert first.report.accepted_attempt == expected_attempt
    assert given_count == expected_givens
    assert given_count <= given_cage_cap(size, profile)  # type: ignore[arg-type]
    assert first.report.given_cage_policy.policy == GIVEN_CAGE_POLICY
    assert first.report.given_cage_policy.accepted_given_cages == given_count
    assert solve(first.puzzle).status == "unique"
    assert parse_puzzle_bytes(serialize_puzzle_bytes(first.puzzle)) == first.puzzle


def test_generation_report_is_versioned_and_deterministic() -> None:
    generated = generate(GenerationConfig(4, 7, "easy"))
    assert count_given_cages(generated.puzzle.cages) <= given_cage_cap(4, "easy")
    data = serialize_generation_report(generated.report)
    report = json.loads(data)
    assert data.endswith(b"\n")
    assert report["schema"] == "kenken.generation-report/v3"
    assert report["size"] == 4
    assert report["requested_profile"] == "easy"
    assert report["evaluated_difficulty"]["band"] == "easy"
    assert report["given_cage_policy"] == {
        "accepted_given_cages": count_given_cages(generated.puzzle.cages),
        "max_given_cages": 4,
        "policy": "given-cap-v1",
    }
    assert report["arithmetic_cage_policy"]["policy"] == ARITHMETIC_CAGE_POLICY
    assert report["arithmetic_cage_policy"]["applicable"] is True
    assert report["arithmetic_cage_policy"]["limits"] == {
        "max_add_target": 18,
        "max_add_terms": 3,
        "max_cage_cells": 3,
        "max_multiply_factors": 2,
        "max_multiply_target": 36,
    }
    assert report["arithmetic_cage_policy"]["accepted_maxima"] is not None
    assert report["accepted_attempt"] == generated.puzzle.provenance.accepted_attempt
    assert sum(report["rejection_counts"].values()) == report["accepted_attempt"] - 1


def test_difficulty_mismatch_is_counted_and_never_accepted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    grid = (
        (1, 2, 3, 4),
        (2, 3, 4, 1),
        (3, 4, 1, 2),
        (4, 1, 2, 3),
    )
    stats = SolveStats(2, 0, 1, 4)
    mismatched = DifficultyResult(
        "search-v1",
        "medium",
        stats,
    )
    monkeypatch.setattr(
        "kenken.generation.generator.latin_grid", lambda size, random: grid
    )
    monkeypatch.setattr(
        "kenken.generation.generator.verify",
        lambda puzzle, max_solver_nodes: (
            VerifiedPuzzle(puzzle, grid, stats),
            SolveResult("unique", 1, grid, stats),
        ),
    )
    monkeypatch.setattr(
        "kenken.generation.generator.evaluate_difficulty",
        lambda puzzle, max_solver_nodes: mismatched,
    )
    monkeypatch.setattr(
        "kenken.generation.generator.evaluate_given_cage_policy",
        lambda size, profile, cages: GivenCagePolicyResult("given-cap-v1", 0, 4, True),
    )
    with pytest.raises(GenerationExhausted) as error:
        generate(GenerationConfig(4, 42, "easy", max_attempts=1))
    assert dict(error.value.report.rejection_counts)["difficulty_mismatch"] == 1
    assert error.value.report.accepted_attempt is None
    assert error.value.report.given_cage_policy.accepted_given_cages is None
    assert sum(dict(error.value.report.rejection_counts).values()) == 1


@pytest.mark.parametrize(
    "config",
    [
        GenerationConfig(4, 0, "easy"),
        GenerationConfig(5, 2**64 - 1, "medium"),
    ],
)
def test_generation_config_valid_boundaries(config: GenerationConfig) -> None:
    assert config.max_attempts == 1_000


@pytest.mark.parametrize(
    "kwargs",
    [
        {"size": 3, "seed": 0, "profile": "easy"},
        {"size": 4, "seed": -1, "profile": "easy"},
        {"size": 4, "seed": 2**64, "profile": "easy"},
        {"size": 4, "seed": 0, "profile": "expert"},
        {"size": 4, "seed": 0, "profile": "easy", "max_attempts": 0},
        {"size": 4, "seed": 0, "profile": "easy", "max_solver_nodes": 0},
        {
            "size": 4,
            "seed": 0,
            "profile": "easy",
            "enabled_operations": ("given",),
        },
    ],
)
def test_generation_config_rejects_invalid_values(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        GenerationConfig(**kwargs)  # type: ignore[arg-type]
