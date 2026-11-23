"""Deterministic candidate generation and search-v1 enforcement."""

from kenken.generation.arithmetic_policy import (
    ARITHMETIC_CAGE_POLICY,
    EASY_ARITHMETIC_LIMITS,
    ArithmeticCageLimits,
    ArithmeticCageMaxima,
    ArithmeticCagePolicyResult,
    arithmetic_cage_limits,
    arithmetic_cage_maxima,
    arithmetic_clue_allowed,
    cage_size_allowed,
    evaluate_arithmetic_cage_policy,
)
from kenken.generation.config import GenerationConfig
from kenken.generation.difficulty import classify_difficulty, evaluate_difficulty
from kenken.generation.generator import (
    ArithmeticCagePolicyReport,
    GeneratedPuzzle,
    GenerationExhausted,
    GenerationReport,
    GivenCagePolicyReport,
    generate,
    serialize_generation_report,
)
from kenken.generation.given_policy import (
    GIVEN_CAGE_POLICY,
    GivenCagePolicyResult,
    count_given_cages,
    evaluate_given_cage_policy,
    given_cage_cap,
)

__all__ = [
    "ARITHMETIC_CAGE_POLICY",
    "EASY_ARITHMETIC_LIMITS",
    "GIVEN_CAGE_POLICY",
    "ArithmeticCageLimits",
    "ArithmeticCageMaxima",
    "ArithmeticCagePolicyReport",
    "ArithmeticCagePolicyResult",
    "GeneratedPuzzle",
    "GenerationConfig",
    "GenerationExhausted",
    "GenerationReport",
    "GivenCagePolicyReport",
    "GivenCagePolicyResult",
    "arithmetic_cage_limits",
    "arithmetic_cage_maxima",
    "arithmetic_clue_allowed",
    "cage_size_allowed",
    "classify_difficulty",
    "count_given_cages",
    "evaluate_arithmetic_cage_policy",
    "evaluate_difficulty",
    "evaluate_given_cage_policy",
    "generate",
    "given_cage_cap",
    "serialize_generation_report",
]
