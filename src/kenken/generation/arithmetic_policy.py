"""Arithmetic-burden limits for generated easy puzzles."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from kenken.model import CageV1, DifficultyBand, Operator

ARITHMETIC_CAGE_POLICY = "arithmetic-cap-v1"


@dataclass(frozen=True)
class ArithmeticCageLimits:
    max_cage_cells: int
    max_add_terms: int
    max_add_target: int
    max_multiply_factors: int
    max_multiply_target: int


@dataclass(frozen=True)
class ArithmeticCageMaxima:
    max_cage_cells: int
    max_add_terms: int | None
    max_add_target: int | None
    max_multiply_factors: int | None
    max_multiply_target: int | None


@dataclass(frozen=True)
class ArithmeticCagePolicyResult:
    policy: str
    applicable: bool
    limits: ArithmeticCageLimits | None
    observed_maxima: ArithmeticCageMaxima
    violating_cages: int
    qualified: bool


EASY_ARITHMETIC_LIMITS = ArithmeticCageLimits(
    max_cage_cells=3,
    max_add_terms=3,
    max_add_target=18,
    max_multiply_factors=2,
    max_multiply_target=36,
)


def _validate_request(size: int, profile: DifficultyBand) -> None:
    if size not in (4, 5, 6) or profile not in ("easy", "medium", "hard"):
        raise ValueError("arithmetic-cage policy requires a supported size and profile")


def arithmetic_cage_limits(
    size: int, profile: DifficultyBand
) -> ArithmeticCageLimits | None:
    """Return the easy limits, or ``None`` when the policy is non-applicable."""
    _validate_request(size, profile)
    return EASY_ARITHMETIC_LIMITS if profile == "easy" else None


def cage_size_allowed(
    size: int,
    profile: DifficultyBand,
    cell_count: int,
    enabled_operations: tuple[Operator, ...],
) -> bool:
    """Whether a cage cardinality has an enabled policy-legal representation."""
    limits = arithmetic_cage_limits(size, profile)
    if limits is None:
        return True
    if cell_count < 1 or cell_count > limits.max_cage_cells:
        return False
    if cell_count == 1:
        return "given" in enabled_operations
    if cell_count == 2:
        return bool(
            set(enabled_operations) & {"add", "subtract", "multiply", "divide"}
        )
    return "add" in enabled_operations


def arithmetic_clue_allowed(
    size: int,
    profile: DifficultyBand,
    operator: Operator,
    target: int,
    cell_count: int,
) -> bool:
    """Whether one exact clue satisfies the applicable arithmetic limits."""
    limits = arithmetic_cage_limits(size, profile)
    if limits is None:
        return True
    if cell_count > limits.max_cage_cells:
        return False
    if operator == "add":
        return (
            cell_count <= limits.max_add_terms and target <= limits.max_add_target
        )
    if operator == "multiply":
        return (
            cell_count <= limits.max_multiply_factors
            and target <= limits.max_multiply_target
        )
    return True


def arithmetic_cage_maxima(cages: Iterable[CageV1]) -> ArithmeticCageMaxima:
    """Derive auditable arithmetic maxima from a non-empty completed partition."""
    materialized = tuple(cages)
    if not materialized:
        raise ValueError("arithmetic-cage policy requires a non-empty cage partition")
    add_cages = tuple(cage for cage in materialized if cage.operator == "add")
    multiply_cages = tuple(
        cage for cage in materialized if cage.operator == "multiply"
    )
    return ArithmeticCageMaxima(
        max_cage_cells=max(len(cage.cells) for cage in materialized),
        max_add_terms=max((len(cage.cells) for cage in add_cages), default=None),
        max_add_target=max((cage.target for cage in add_cages), default=None),
        max_multiply_factors=max(
            (len(cage.cells) for cage in multiply_cages), default=None
        ),
        max_multiply_target=max(
            (cage.target for cage in multiply_cages), default=None
        ),
    )


def evaluate_arithmetic_cage_policy(
    size: int, profile: DifficultyBand, cages: Iterable[CageV1]
) -> ArithmeticCagePolicyResult:
    """Evaluate a completed normalized partition against arithmetic-cap-v1."""
    materialized = tuple(cages)
    maxima = arithmetic_cage_maxima(materialized)
    limits = arithmetic_cage_limits(size, profile)
    violations = (
        sum(
            not arithmetic_clue_allowed(
                size, profile, cage.operator, cage.target, len(cage.cells)
            )
            for cage in materialized
        )
        if limits is not None
        else 0
    )
    return ArithmeticCagePolicyResult(
        policy=ARITHMETIC_CAGE_POLICY,
        applicable=limits is not None,
        limits=limits,
        observed_maxima=maxima,
        violating_cages=violations,
        qualified=violations == 0,
    )
