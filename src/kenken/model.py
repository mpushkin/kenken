"""Immutable domain and result types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

type Operator = Literal["given", "add", "subtract", "multiply", "divide"]
type SolveStatus = Literal["unsatisfiable", "unique", "multiple", "unknown"]
type SolveOneStatus = Literal["solved", "unsatisfiable", "unknown"]
type Grid = tuple[tuple[int, ...], ...]
type DifficultyBand = Literal["easy", "medium", "hard"]

DEFAULT_MAX_SOLVER_NODES = 1_000_000


@dataclass(frozen=True, order=True)
class CellV1:
    row: int
    column: int


@dataclass(frozen=True)
class CageV1:
    target: int
    operator: Operator
    cells: tuple[CellV1, ...]


@dataclass(frozen=True)
class ProvenanceV1:
    generator_version: str
    seed: str
    profile: str
    accepted_attempt: int


@dataclass(frozen=True)
class PuzzleDefinitionV1:
    schema: str
    id: str
    size: int
    cages: tuple[CageV1, ...]
    provenance: ProvenanceV1 | None = None


@dataclass(frozen=True)
class SolutionV1:
    schema: str
    puzzle_id: str
    grid: Grid


@dataclass(frozen=True)
class SolverBudget:
    max_solver_nodes: int = DEFAULT_MAX_SOLVER_NODES

    def __post_init__(self) -> None:
        if (
            isinstance(self.max_solver_nodes, bool)
            or not isinstance(self.max_solver_nodes, int)
            or self.max_solver_nodes <= 0
        ):
            raise ValueError("max_solver_nodes must be a positive integer")


@dataclass(frozen=True)
class SolveStats:
    visited_nodes: int
    backtracks: int
    max_decision_depth: int
    propagation_rounds: int


@dataclass(frozen=True)
class SolveResult:
    status: SolveStatus
    solutions_found: Literal[0, 1, 2]
    first_solution: Grid | None
    stats: SolveStats


@dataclass(frozen=True)
class SolveOneResult:
    status: SolveOneStatus
    solution: Grid | None
    stats: SolveStats


@dataclass(frozen=True)
class VerifiedPuzzle:
    definition: PuzzleDefinitionV1
    solution: Grid
    stats: SolveStats


@dataclass(frozen=True)
class DifficultyResult:
    policy: Literal["search-v1"]
    band: DifficultyBand
    stats: SolveStats
