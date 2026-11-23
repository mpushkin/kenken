"""Bounded deterministic generation with uniqueness and difficulty gates."""

from __future__ import annotations

import json
from dataclasses import dataclass

from kenken.generation.arithmetic_policy import (
    ARITHMETIC_CAGE_POLICY,
    ArithmeticCageLimits,
    ArithmeticCageMaxima,
    arithmetic_cage_limits,
    evaluate_arithmetic_cage_policy,
)
from kenken.generation.cages import build_cages
from kenken.generation.config import GenerationConfig
from kenken.generation.difficulty import evaluate_difficulty
from kenken.generation.given_policy import (
    GIVEN_CAGE_POLICY,
    evaluate_given_cage_policy,
    given_cage_cap,
)
from kenken.generation.latin import latin_grid
from kenken.model import DifficultyResult, Grid, ProvenanceV1, PuzzleDefinitionV1
from kenken.randomness import RandomV1
from kenken.serialization import compute_puzzle_id
from kenken.solver import verify
from kenken.validation import ValidationError, validate_puzzle_structure

GENERATOR_VERSION = "0.3.0"
_REASONS = (
    "invalid",
    "given_limit_exceeded",
    "arithmetic_limit_exceeded",
    "unsatisfiable",
    "multiple",
    "unknown",
    "solution_mismatch",
    "difficulty_mismatch",
)


@dataclass(frozen=True)
class GivenCagePolicyReport:
    policy: str
    max_given_cages: int
    accepted_given_cages: int | None


@dataclass(frozen=True)
class ArithmeticCagePolicyReport:
    policy: str
    applicable: bool
    limits: ArithmeticCageLimits | None
    accepted_maxima: ArithmeticCageMaxima | None


@dataclass(frozen=True)
class GenerationReport:
    seed: int
    size: int
    requested_profile: str
    attempts: int
    accepted_attempt: int | None
    evaluated_difficulty: DifficultyResult | None
    given_cage_policy: GivenCagePolicyReport
    arithmetic_cage_policy: ArithmeticCagePolicyReport
    rejection_counts: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class GeneratedPuzzle:
    puzzle: PuzzleDefinitionV1
    solution: Grid
    difficulty: DifficultyResult
    report: GenerationReport


class GenerationExhausted(RuntimeError):
    def __init__(self, report: GenerationReport) -> None:
        super().__init__(f"generation exhausted after {report.attempts} attempts")
        self.report = report


def generate(config: GenerationConfig) -> GeneratedPuzzle:
    random = RandomV1(config.seed)
    counts = {reason: 0 for reason in _REASONS}
    for attempt in range(1, config.max_attempts + 1):
        grid = latin_grid(config.size, random)
        cages = build_cages(
            grid,
            config.profile,
            random,
            config.enabled_operations,
        )
        bare = PuzzleDefinitionV1("kenken.puzzle/v1", "placeholder", config.size, cages)
        try:
            puzzle_id = compute_puzzle_id(bare)
            candidate = PuzzleDefinitionV1(
                bare.schema,
                puzzle_id,
                bare.size,
                bare.cages,
                ProvenanceV1(GENERATOR_VERSION, str(config.seed), config.profile, attempt),
            )
            validate_puzzle_structure(candidate)
        except ValidationError:
            counts["invalid"] += 1
            continue

        given_policy = evaluate_given_cage_policy(
            config.size, config.profile, candidate.cages
        )
        if not given_policy.qualified:
            counts["given_limit_exceeded"] += 1
            continue

        arithmetic_policy = evaluate_arithmetic_cage_policy(
            config.size, config.profile, candidate.cages
        )
        if not arithmetic_policy.qualified:
            counts["arithmetic_limit_exceeded"] += 1
            continue

        verified, solve_result = verify(candidate, config.max_solver_nodes)
        if verified is None:
            counts[solve_result.status] += 1
            continue
        if verified.solution != grid:
            counts["solution_mismatch"] += 1
            continue
        difficulty = evaluate_difficulty(candidate, config.max_solver_nodes)
        if difficulty is None:
            counts["unknown"] += 1
            continue
        if difficulty.band != config.profile:
            counts["difficulty_mismatch"] += 1
            continue
        final_given_policy = evaluate_given_cage_policy(
            config.size, config.profile, candidate.cages
        )
        if not final_given_policy.qualified:
            raise AssertionError("accepted candidate violates given-cap-v1")
        final_arithmetic_policy = evaluate_arithmetic_cage_policy(
            config.size, config.profile, candidate.cages
        )
        if not final_arithmetic_policy.qualified:
            raise AssertionError("accepted candidate violates arithmetic-cap-v1")
        report = _report(
            config,
            attempt,
            attempt,
            difficulty,
            final_given_policy.given_cages,
            final_arithmetic_policy.observed_maxima,
            counts,
        )
        return GeneratedPuzzle(candidate, grid, difficulty, report)
    raise GenerationExhausted(
        _report(config, config.max_attempts, None, None, None, None, counts)
    )


def _report(
    config: GenerationConfig,
    attempts: int,
    accepted_attempt: int | None,
    difficulty: DifficultyResult | None,
    accepted_given_cages: int | None,
    accepted_arithmetic_maxima: ArithmeticCageMaxima | None,
    counts: dict[str, int],
) -> GenerationReport:
    return GenerationReport(
        seed=config.seed,
        size=config.size,
        requested_profile=config.profile,
        attempts=attempts,
        accepted_attempt=accepted_attempt,
        evaluated_difficulty=difficulty,
        given_cage_policy=GivenCagePolicyReport(
            policy=GIVEN_CAGE_POLICY,
            max_given_cages=given_cage_cap(config.size, config.profile),
            accepted_given_cages=accepted_given_cages,
        ),
        arithmetic_cage_policy=ArithmeticCagePolicyReport(
            policy=ARITHMETIC_CAGE_POLICY,
            applicable=config.profile == "easy",
            limits=arithmetic_cage_limits(config.size, config.profile),
            accepted_maxima=accepted_arithmetic_maxima,
        ),
        rejection_counts=tuple((reason, counts[reason]) for reason in _REASONS),
    )


def serialize_generation_report(report: GenerationReport) -> bytes:
    difficulty: dict[str, object] | None = None
    if report.evaluated_difficulty is not None:
        item = report.evaluated_difficulty
        difficulty = {
            "policy": item.policy,
            "band": item.band,
            "stats": {
                "visited_nodes": item.stats.visited_nodes,
                "backtracks": item.stats.backtracks,
                "max_decision_depth": item.stats.max_decision_depth,
                "propagation_rounds": item.stats.propagation_rounds,
            },
        }
    limits = report.arithmetic_cage_policy.limits
    maxima = report.arithmetic_cage_policy.accepted_maxima
    value = {
        "schema": "kenken.generation-report/v3",
        "seed": str(report.seed),
        "size": report.size,
        "requested_profile": report.requested_profile,
        "attempts": report.attempts,
        "accepted_attempt": report.accepted_attempt,
        "evaluated_difficulty": difficulty,
        "given_cage_policy": {
            "policy": report.given_cage_policy.policy,
            "max_given_cages": report.given_cage_policy.max_given_cages,
            "accepted_given_cages": report.given_cage_policy.accepted_given_cages,
        },
        "arithmetic_cage_policy": {
            "policy": report.arithmetic_cage_policy.policy,
            "applicable": report.arithmetic_cage_policy.applicable,
            "limits": _arithmetic_values(limits),
            "accepted_maxima": _arithmetic_values(maxima),
        },
        "rejection_counts": dict(report.rejection_counts),
    }
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _arithmetic_values(
    value: ArithmeticCageLimits | ArithmeticCageMaxima | None,
) -> dict[str, int | None] | None:
    if value is None:
        return None
    return {
        "max_cage_cells": value.max_cage_cells,
        "max_add_terms": value.max_add_terms,
        "max_add_target": value.max_add_target,
        "max_multiply_factors": value.max_multiply_factors,
        "max_multiply_target": value.max_multiply_target,
    }
