"""Hard singleton-given limits for generated difficulty profiles."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from kenken.model import CageV1, DifficultyBand

GIVEN_CAGE_POLICY = "given-cap-v1"

_GIVEN_CAPS: dict[int, dict[DifficultyBand, int]] = {
    size: {"easy": 4, "medium": 2, "hard": 1} for size in (4, 5, 6)
}


@dataclass(frozen=True)
class GivenCagePolicyResult:
    policy: str
    given_cages: int
    max_given_cages: int
    qualified: bool


def given_cage_cap(size: int, profile: DifficultyBand) -> int:
    """Return the inclusive given-cage cap for a supported generation request."""
    try:
        return _GIVEN_CAPS[size][profile]
    except KeyError as error:
        raise ValueError("given-cage policy requires a supported size and profile") from error


def count_given_cages(cages: Iterable[CageV1]) -> int:
    """Count normalized cages whose operator is ``given``."""
    return sum(cage.operator == "given" for cage in cages)


def evaluate_given_cage_policy(
    size: int, profile: DifficultyBand, cages: Iterable[CageV1]
) -> GivenCagePolicyResult:
    """Evaluate a completed cage partition against given-cap-v1."""
    given_cages = count_given_cages(cages)
    maximum = given_cage_cap(size, profile)
    return GivenCagePolicyResult(
        policy=GIVEN_CAGE_POLICY,
        given_cages=given_cages,
        max_given_cages=maximum,
        qualified=given_cages <= maximum,
    )
