from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from hypothesis import given
from hypothesis import strategies as st
from jsonschema.validators import Draft202012Validator

from kenken.generation import (
    GenerationConfig,
    GenerationExhausted,
    count_given_cages,
    evaluate_given_cage_policy,
    generate,
    given_cage_cap,
    serialize_generation_report,
)
from kenken.generation.cages import build_cages
from kenken.generation.latin import latin_grid
from kenken.model import CageV1, CellV1, DifficultyBand, Grid
from kenken.randomness import RandomV1

_CAPS = {"easy": 4, "medium": 2, "hard": 1}
SCHEMAS = Path(__file__).parents[2] / "schemas"
REPORT_V3_SCHEMA = json.loads(
    (SCHEMAS / "kenken-generation-report-v3.schema.json").read_text()
)
Draft202012Validator.check_schema(REPORT_V3_SCHEMA)
REPORT_V3_VALIDATOR = Draft202012Validator(REPORT_V3_SCHEMA)


def _assert_report_v3_contract(data: bytes, *, successful: bool) -> dict[str, Any]:
    assert data.endswith(b"\n")
    report = json.loads(data)
    REPORT_V3_VALIDATOR.validate(report)
    rejection_total = sum(report["rejection_counts"].values())
    if successful:
        assert report["accepted_attempt"] is not None
        assert report["evaluated_difficulty"] is not None
        assert report["given_cage_policy"]["accepted_given_cages"] is not None
        assert report["arithmetic_cage_policy"]["accepted_maxima"] is not None
        assert rejection_total == report["accepted_attempt"] - 1
    else:
        assert report["accepted_attempt"] is None
        assert report["evaluated_difficulty"] is None
        assert report["given_cage_policy"]["accepted_given_cages"] is None
        assert report["arithmetic_cage_policy"]["accepted_maxima"] is None
        assert rejection_total == report["attempts"]
    return cast(dict[str, Any], report)


@pytest.mark.parametrize("size", [4, 5, 6])
@pytest.mark.parametrize("profile", ["easy", "medium", "hard"])
def test_given_cap_v1_exact_table_and_boundary(
    size: int, profile: DifficultyBand
) -> None:
    cap = given_cage_cap(size, profile)
    assert cap == _CAPS[profile]
    cells = tuple(CellV1(index // size, index % size) for index in range(cap + 1))
    at_cap = tuple(CageV1(index + 1, "given", (cell,)) for index, cell in enumerate(cells[:cap]))
    above_cap = (*at_cap, CageV1(cap + 1, "given", (cells[cap],)))

    accepted = evaluate_given_cage_policy(size, profile, at_cap)
    rejected = evaluate_given_cage_policy(size, profile, above_cap)
    assert accepted.policy == "given-cap-v1"
    assert accepted.given_cages == cap
    assert accepted.max_given_cages == cap
    assert accepted.qualified
    assert rejected.given_cages == cap + 1
    assert not rejected.qualified


@pytest.mark.parametrize("size", [4, 5, 6])
def test_given_caps_are_monotonic_by_profile(size: int) -> None:
    assert (
        given_cage_cap(size, "easy")
        >= given_cage_cap(size, "medium")
        >= given_cage_cap(size, "hard")
    )


@given(
    size=st.sampled_from((4, 5, 6)),
    profile=st.sampled_from(("easy", "medium", "hard")),
    given_count=st.integers(min_value=0, max_value=36),
)
def test_given_policy_qualification_is_exact_upper_bound(
    size: int, profile: DifficultyBand, given_count: int
) -> None:
    bounded_count = min(given_count, size * size)
    cages = tuple(
        CageV1(
            index % size + 1,
            "given",
            (CellV1(index // size, index % size),),
        )
        for index in range(bounded_count)
    )
    result = evaluate_given_cage_policy(size, profile, cages)
    assert result.given_cages == bounded_count
    assert result.qualified is (bounded_count <= given_cage_cap(size, profile))


class _RecordingRandom:
    def __init__(self) -> None:
        self.size_choices: list[tuple[int, ...]] = []

    def randbelow(self, upper: int) -> int:
        assert upper > 0
        return 0

    def choice(self, values: Any) -> Any:
        choices = tuple(values)
        if choices and isinstance(choices[0], int):
            self.size_choices.append(cast(tuple[int, ...], choices))
        return choices[0]


def test_construction_stops_intentional_singleton_selection_at_cap() -> None:
    grid: Grid = (
        (1, 2, 3, 4),
        (2, 3, 4, 1),
        (3, 4, 1, 2),
        (4, 1, 2, 3),
    )
    random = _RecordingRandom()
    cages = build_cages(
        grid,
        "easy",
        cast(Any, random),
        ("given", "add", "multiply"),
    )
    assert count_given_cages(cages) == 4
    assert random.size_choices[:4] == [
        (1, 2, 2, 2, 3, 3),
        (1, 2, 2, 2, 3, 3),
        (1, 2, 2, 2, 3, 3),
        (1, 2, 2, 2, 3, 3),
    ]
    assert all(1 not in choices for choices in random.size_choices[4:])


def test_blocked_growth_can_exceed_construction_bias_and_final_gate_rejects() -> None:
    random = RandomV1(1)
    grid = latin_grid(4, random)
    cages = build_cages(
        grid,
        "easy",
        random,
        ("given", "add", "subtract", "multiply", "divide"),
    )
    assert count_given_cages(cages) == 5

    with pytest.raises(GenerationExhausted) as error:
        generate(GenerationConfig(4, 1, "easy", max_attempts=1))
    assert dict(error.value.report.rejection_counts)["given_limit_exceeded"] == 1


def test_over_cap_partition_is_rejected_before_solver_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    grid: Grid = (
        (1, 2, 3, 4),
        (2, 3, 4, 1),
        (3, 4, 1, 2),
        (4, 1, 2, 3),
    )
    cages = tuple(
        CageV1(grid[row][column], "given", (CellV1(row, column),))
        for row in range(4)
        for column in range(4)
    )

    monkeypatch.setattr("kenken.generation.generator.latin_grid", lambda size, random: grid)
    monkeypatch.setattr(
        "kenken.generation.generator.build_cages",
        lambda grid, profile, random, enabled_operations: cages,
    )

    def unexpected(*args: object, **kwargs: object) -> None:
        raise AssertionError("solver and difficulty gates must not run")

    monkeypatch.setattr("kenken.generation.generator.verify", unexpected)
    monkeypatch.setattr("kenken.generation.generator.evaluate_difficulty", unexpected)

    with pytest.raises(GenerationExhausted) as error:
        generate(GenerationConfig(4, 42, "easy", max_attempts=1))
    report = error.value.report
    assert dict(report.rejection_counts)["given_limit_exceeded"] == 1
    assert report.accepted_attempt is None
    assert report.evaluated_difficulty is None
    assert report.given_cage_policy.max_given_cages == 4
    assert report.given_cage_policy.accepted_given_cages is None
    serialized = serialize_generation_report(report)
    payload = _assert_report_v3_contract(serialized, successful=False)
    assert payload["schema"] == "kenken.generation-report/v3"
    assert payload["rejection_counts"]["given_limit_exceeded"] == 1


def test_successful_report_fully_validates_against_v3_schema() -> None:
    generated = generate(GenerationConfig(4, 7, "easy"))
    observed_givens = count_given_cages(generated.puzzle.cages)
    assert observed_givens <= given_cage_cap(4, "easy")
    report = _assert_report_v3_contract(
        serialize_generation_report(generated.report), successful=True
    )
    assert report["given_cage_policy"]["accepted_given_cages"] == observed_givens


@pytest.mark.parametrize(
    "enabled_operations",
    [("given", "add"), ("given", "multiply")],
)
def test_valid_operation_subsets_cannot_bypass_cap(
    enabled_operations: tuple[str, ...],
) -> None:
    generated = generate(
        GenerationConfig(
            4,
            42,
            "easy",
            enabled_operations=cast(Any, enabled_operations),
        )
    )
    assert count_given_cages(generated.puzzle.cages) <= given_cage_cap(4, "easy")
