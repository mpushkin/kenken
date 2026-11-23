"""Validated public generation configuration."""

from __future__ import annotations

from dataclasses import dataclass

from kenken.model import DifficultyBand, Operator, SolverBudget


@dataclass(frozen=True)
class GenerationConfig:
    size: int
    seed: int
    profile: DifficultyBand
    max_attempts: int = 1_000
    max_solver_nodes: int = 1_000_000
    enabled_operations: tuple[Operator, ...] = (
        "given",
        "add",
        "subtract",
        "multiply",
        "divide",
    )

    def __post_init__(self) -> None:
        if (
            isinstance(self.size, bool)
            or not isinstance(self.size, int)
            or self.size not in (4, 5, 6)
        ):
            raise ValueError("generation size must be 4, 5, or 6")
        if (
            isinstance(self.seed, bool)
            or not isinstance(self.seed, int)
            or not 0 <= self.seed <= 2**64 - 1
        ):
            raise ValueError("seed must be a uint64")
        if self.profile not in ("easy", "medium", "hard"):
            raise ValueError("profile must be easy, medium, or hard")
        if (
            isinstance(self.max_attempts, bool)
            or not isinstance(self.max_attempts, int)
            or self.max_attempts <= 0
        ):
            raise ValueError("max_attempts must be a positive integer")
        SolverBudget(self.max_solver_nodes)
        supported = {"given", "add", "subtract", "multiply", "divide"}
        if (
            len(set(self.enabled_operations)) != len(self.enabled_operations)
            or not set(self.enabled_operations) <= supported
            or "given" not in self.enabled_operations
            or not set(self.enabled_operations) & {"add", "multiply"}
        ):
            raise ValueError(
                "enabled_operations must be unique supported operators including "
                "given and at least one of add or multiply"
            )
