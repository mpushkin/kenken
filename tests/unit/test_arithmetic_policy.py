from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from hypothesis import given
from hypothesis import strategies as st
from jsonschema.validators import Draft202012Validator

from kenken.generation import (
    ARITHMETIC_CAGE_POLICY,
    EASY_ARITHMETIC_LIMITS,
    GenerationConfig,
    GenerationExhausted,
    arithmetic_cage_limits,
    arithmetic_clue_allowed,
    evaluate_arithmetic_cage_policy,
    generate,
    serialize_generation_report,
)
from kenken.model import CageV1, CellV1, DifficultyBand, Grid, Operator
from kenken.serialization import parse_puzzle_bytes
from kenken.solver import verify

ROOT = Path(__file__).parents[2]
REPORT_V3 = json.loads(
    (ROOT / "schemas" / "kenken-generation-report-v3.schema.json").read_text()
)
REPORT_V2 = json.loads(
    (ROOT / "schemas" / "kenken-generation-report-v2.schema.json").read_text()
)


def _cells(count: int, *, start: int = 0) -> tuple[CellV1, ...]:
    return tuple(CellV1((start + index) // 6, (start + index) % 6) for index in range(count))


@pytest.mark.parametrize("size", [4, 5, 6])
def test_exact_easy_limits_and_non_applicable_profiles(size: int) -> None:
    assert arithmetic_cage_limits(size, "easy") == EASY_ARITHMETIC_LIMITS
    assert (
        type(EASY_ARITHMETIC_LIMITS)(
            max_cage_cells=3,
            max_add_terms=3,
            max_add_target=18,
            max_multiply_factors=2,
            max_multiply_target=36,
        )
    ) == EASY_ARITHMETIC_LIMITS
    cages = (CageV1(100, "multiply", _cells(4)),)
    for profile in ("medium", "hard"):
        result = evaluate_arithmetic_cage_policy(
            size, cast(DifficultyBand, profile), cages
        )
        assert result.policy == ARITHMETIC_CAGE_POLICY
        assert not result.applicable
        assert result.limits is None
        assert result.violating_cages == 0
        assert result.qualified
        assert result.observed_maxima.max_multiply_target == 100


@pytest.mark.parametrize(
    ("cage", "qualified"),
    [
        (CageV1(36, "multiply", _cells(2)), True),
        (CageV1(37, "multiply", _cells(2)), False),
        (CageV1(24, "multiply", _cells(3)), False),
        (CageV1(18, "add", _cells(3)), True),
        (CageV1(19, "add", _cells(3)), False),
        (CageV1(10, "add", _cells(4)), False),
    ],
)
def test_easy_arithmetic_boundaries(cage: CageV1, qualified: bool) -> None:
    result = evaluate_arithmetic_cage_policy(6, "easy", (cage,))
    assert result.qualified is qualified
    assert result.violating_cages == (0 if qualified else 1)


@given(
    cages=st.lists(
        st.tuples(
            st.sampled_from(("given", "add", "subtract", "multiply", "divide")),
            st.integers(min_value=1, max_value=50),
            st.integers(min_value=1, max_value=4),
        ),
        min_size=1,
        max_size=12,
    )
)
def test_qualification_matches_distinct_violating_cages(
    cages: list[tuple[Operator, int, int]],
) -> None:
    materialized = tuple(
        CageV1(target, operator, _cells(count))
        for operator, target, count in cages
    )
    expected = sum(
        not arithmetic_clue_allowed(6, "easy", operator, target, count)
        for operator, target, count in cages
    )
    result = evaluate_arithmetic_cage_policy(6, "easy", materialized)
    assert result.violating_cages == expected
    assert result.qualified is (expected == 0)


@pytest.mark.parametrize("size", [4, 5, 6])
@pytest.mark.parametrize(
    "enabled_operations",
    [("given", "add"), ("given", "multiply")],
)
def test_easy_operation_subsets_remain_bounded_and_policy_qualified(
    size: int, enabled_operations: tuple[Operator, ...]
) -> None:
    generated = generate(
        GenerationConfig(
            size,
            42,
            "easy",
            enabled_operations=enabled_operations,
        )
    )
    policy = evaluate_arithmetic_cage_policy(size, "easy", generated.puzzle.cages)
    assert policy.qualified
    assert all(len(cage.cells) <= 3 for cage in generated.puzzle.cages)
    assert all(
        len(cage.cells) == 2
        for cage in generated.puzzle.cages
        if cage.operator == "multiply"
    )
    assert all(
        cage.operator == "add"
        for cage in generated.puzzle.cages
        if len(cage.cells) == 3
    )


def _latin_grid() -> Grid:
    return (
        (1, 2, 3, 4),
        (2, 3, 4, 1),
        (3, 4, 1, 2),
        (4, 1, 2, 3),
    )


def _row_add_cages() -> tuple[CageV1, ...]:
    return tuple(
        CageV1(10, "add", tuple(CellV1(row, column) for column in range(4)))
        for row in range(4)
    )


def test_arithmetic_gate_rejects_before_solver_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "kenken.generation.generator.latin_grid", lambda size, random: _latin_grid()
    )
    monkeypatch.setattr(
        "kenken.generation.generator.build_cages",
        lambda grid, profile, random, enabled_operations: _row_add_cages(),
    )

    def unexpected(*args: object, **kwargs: object) -> None:
        raise AssertionError("solver and difficulty gates must not run")

    monkeypatch.setattr("kenken.generation.generator.verify", unexpected)
    monkeypatch.setattr("kenken.generation.generator.evaluate_difficulty", unexpected)

    with pytest.raises(GenerationExhausted) as error:
        generate(GenerationConfig(4, 42, "easy", max_attempts=1))
    report = error.value.report
    assert dict(report.rejection_counts)["arithmetic_limit_exceeded"] == 1
    assert report.arithmetic_cage_policy.accepted_maxima is None


def test_given_gate_wins_attribution_when_both_policies_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    grid = _latin_grid()
    cages = (
        CageV1(10, "add", tuple(CellV1(0, column) for column in range(4))),
        *(
            CageV1(grid[row][column], "given", (CellV1(row, column),))
            for row in range(1, 4)
            for column in range(4)
        ),
    )
    monkeypatch.setattr(
        "kenken.generation.generator.latin_grid", lambda size, random: grid
    )
    monkeypatch.setattr(
        "kenken.generation.generator.build_cages",
        lambda grid, profile, random, enabled_operations: cages,
    )
    with pytest.raises(GenerationExhausted) as error:
        generate(GenerationConfig(4, 42, "easy", max_attempts=1))
    counts = dict(error.value.report.rejection_counts)
    assert counts["given_limit_exceeded"] == 1
    assert counts["arithmetic_limit_exceeded"] == 0


def test_arithmetic_policy_is_reasserted_before_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from kenken.generation import generator

    real_evaluator = generator.evaluate_arithmetic_cage_policy
    calls = 0

    def recording_evaluator(*args: Any, **kwargs: Any) -> Any:
        nonlocal calls
        calls += 1
        return real_evaluator(*args, **kwargs)

    monkeypatch.setattr(generator, "evaluate_arithmetic_cage_policy", recording_evaluator)
    generate(GenerationConfig(4, 42, "easy"))
    assert calls == 2


@pytest.mark.parametrize("profile", ["easy", "medium", "hard"])
def test_success_reports_validate_against_v3(
    profile: DifficultyBand,
) -> None:
    generated = generate(
        GenerationConfig(4, 42, profile, max_attempts=2_000)
    )
    report = json.loads(serialize_generation_report(generated.report))
    Draft202012Validator(REPORT_V3).validate(report)
    assert report["schema"] == "kenken.generation-report/v3"
    assert report["arithmetic_cage_policy"]["accepted_maxima"] is not None
    assert report["arithmetic_cage_policy"]["applicable"] is (profile == "easy")
    assert (report["arithmetic_cage_policy"]["limits"] is not None) is (
        profile == "easy"
    )


def test_retained_v2_report_and_historical_puzzle_remain_valid(collection_project: Path) -> None:
    sources = collection_project / "output" / "pdf" / "volume-2" / "sources"
    stem = "page-01-4x4-easy-puzzle-01-seed-2026072601"
    report_path = sources / f"{stem}.report.json"
    puzzle_path = sources / f"{stem}.puzzle.json"
    Draft202012Validator(REPORT_V2).validate(json.loads(report_path.read_text()))
    puzzle = parse_puzzle_bytes(puzzle_path.read_bytes())
    verified, result = verify(puzzle)
    assert verified is not None
    assert result.status == "unique"
    assert not evaluate_arithmetic_cage_policy(4, "easy", puzzle.cages).qualified
