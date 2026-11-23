"""The experimental search-v1 difficulty policy."""

from __future__ import annotations

from kenken.model import DifficultyBand, DifficultyResult, PuzzleDefinitionV1, SolveStats
from kenken.solver import solve_one


def classify_difficulty(stats: SolveStats) -> DifficultyBand:
    if stats.max_decision_depth == 0:
        return "easy"
    if stats.max_decision_depth <= 2 and stats.visited_nodes <= 100:
        return "medium"
    return "hard"


def evaluate_difficulty(
    puzzle: PuzzleDefinitionV1, max_solver_nodes: int = 1_000_000
) -> DifficultyResult | None:
    result = solve_one(puzzle, max_solver_nodes)
    if result.status != "solved":
        return None
    return DifficultyResult("search-v1", classify_difficulty(result.stats), result.stats)
