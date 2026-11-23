"""Deterministic bounded exact solver."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from kenken.model import (
    Grid,
    PuzzleDefinitionV1,
    SolveOneResult,
    SolveOneStatus,
    SolverBudget,
    SolveResult,
    SolveStats,
    SolveStatus,
    VerifiedPuzzle,
)
from kenken.validation import cage_tuples, validate_puzzle_structure


@dataclass
class _Counters:
    visited_nodes: int = 0
    backtracks: int = 0
    max_decision_depth: int = 0
    propagation_rounds: int = 0

    def freeze(self) -> SolveStats:
        return SolveStats(
            visited_nodes=self.visited_nodes,
            backtracks=self.backtracks,
            max_decision_depth=self.max_decision_depth,
            propagation_rounds=self.propagation_rounds,
        )


@dataclass(frozen=True)
class _CageConstraint:
    indexes: tuple[int, ...]
    tuples: tuple[tuple[int, ...], ...]


@dataclass
class _Search:
    size: int
    cages: tuple[_CageConstraint, ...]
    budget: SolverBudget
    solution_limit: int
    counters: _Counters
    solutions: list[Grid]
    exhausted: bool = False

    def run(self) -> bool:
        values = set(range(1, self.size + 1))
        domains = [set(values) for _ in range(self.size * self.size)]
        return self._visit(domains, 0)

    def _visit(self, domains: list[set[int]], depth: int) -> bool:
        if self.counters.visited_nodes >= self.budget.max_solver_nodes:
            self.exhausted = True
            return False
        self.counters.visited_nodes += 1
        self.counters.max_decision_depth = max(self.counters.max_decision_depth, depth)

        if not self._propagate(domains):
            return True
        if all(len(domain) == 1 for domain in domains):
            self.solutions.append(_to_grid(domains, self.size))
            return True

        index = min(
            (index for index, domain in enumerate(domains) if len(domain) > 1),
            key=lambda item: (len(domains[item]), item),
        )
        for value in sorted(domains[index]):
            before = len(self.solutions)
            child = [set(domain) for domain in domains]
            child[index] = {value}
            completed = self._visit(child, depth + 1)
            if completed and len(self.solutions) == before:
                self.counters.backtracks += 1
            if len(self.solutions) >= self.solution_limit:
                return True
            if not completed:
                return False
        return True

    def _propagate(self, domains: list[set[int]]) -> bool:
        while True:
            changed, valid = self._sweep(domains)
            self.counters.propagation_rounds += 1
            if not valid:
                return False
            if not changed:
                return True

    def _sweep(self, domains: list[set[int]]) -> tuple[bool, bool]:
        changed = False
        valid = True
        units = [
            tuple(row * self.size + column for column in range(self.size))
            for row in range(self.size)
        ]
        units.extend(
            tuple(row * self.size + column for row in range(self.size))
            for column in range(self.size)
        )

        for unit in units:
            singletons = [next(iter(domains[index])) for index in unit if len(domains[index]) == 1]
            if len(singletons) != len(set(singletons)):
                valid = False
            fixed = set(singletons)
            for index in unit:
                if len(domains[index]) > 1:
                    reduced = domains[index] - fixed
                    if reduced != domains[index]:
                        domains[index] = reduced
                        changed = True
                    if not reduced:
                        valid = False
            for value in range(1, self.size + 1):
                places = [index for index in unit if value in domains[index]]
                if not places:
                    valid = False
                elif len(places) == 1 and domains[places[0]] != {value}:
                    domains[places[0]] = {value}
                    changed = True

        for cage in self.cages:
            possible = tuple(
                values
                for values in cage.tuples
                if all(
                    value in domains[index]
                    for index, value in zip(cage.indexes, values, strict=True)
                )
            )
            if not possible:
                valid = False
                continue
            for position, index in enumerate(cage.indexes):
                allowed = {values[position] for values in possible}
                reduced = domains[index] & allowed
                if reduced != domains[index]:
                    domains[index] = reduced
                    changed = True
                if not reduced:
                    valid = False

        return changed, valid


def _constraints(puzzle: PuzzleDefinitionV1) -> tuple[_CageConstraint, ...]:
    return tuple(
        _CageConstraint(
            indexes=tuple(cell.row * puzzle.size + cell.column for cell in cage.cells),
            tuples=cage_tuples(puzzle.size, cage),
        )
        for cage in puzzle.cages
    )


def _to_grid(domains: list[set[int]], size: int) -> Grid:
    return tuple(
        tuple(next(iter(domains[row * size + column])) for column in range(size))
        for row in range(size)
    )


def solve(
    puzzle: PuzzleDefinitionV1,
    max_solver_nodes: int = 1_000_000,
) -> SolveResult:
    """Count up to two solutions within a required positive node budget."""
    budget = SolverBudget(max_solver_nodes)
    validate_puzzle_structure(puzzle)
    search = _Search(
        size=puzzle.size,
        cages=_constraints(puzzle),
        budget=budget,
        solution_limit=2,
        counters=_Counters(),
        solutions=[],
    )
    completed = search.run()
    found = min(len(search.solutions), 2)
    solutions_found: Literal[0, 1, 2] = 2 if found == 2 else 1 if found == 1 else 0
    status: SolveStatus
    if found == 2:
        status = "multiple"
    elif not completed or search.exhausted:
        status = "unknown"
    elif found == 1:
        status = "unique"
    else:
        status = "unsatisfiable"
    return SolveResult(
        status=status,
        solutions_found=solutions_found,
        first_solution=search.solutions[0] if search.solutions else None,
        stats=search.counters.freeze(),
    )


def solve_one(
    puzzle: PuzzleDefinitionV1,
    max_solver_nodes: int = 1_000_000,
) -> SolveOneResult:
    """Run an independently counted deterministic traversal stopping at one solution."""
    budget = SolverBudget(max_solver_nodes)
    validate_puzzle_structure(puzzle)
    search = _Search(
        size=puzzle.size,
        cages=_constraints(puzzle),
        budget=budget,
        solution_limit=1,
        counters=_Counters(),
        solutions=[],
    )
    completed = search.run()
    status: SolveOneStatus
    if search.solutions:
        status = "solved"
        solution = search.solutions[0]
    elif not completed or search.exhausted:
        status = "unknown"
        solution = None
    else:
        status = "unsatisfiable"
        solution = None
    return SolveOneResult(status=status, solution=solution, stats=search.counters.freeze())


def verify(
    puzzle: PuzzleDefinitionV1,
    max_solver_nodes: int = 1_000_000,
) -> tuple[VerifiedPuzzle | None, SolveResult]:
    """Construct a VerifiedPuzzle capability only after a bounded uniqueness proof."""
    result = solve(puzzle, max_solver_nodes)
    if result.status != "unique" or result.first_solution is None:
        return None, result
    return (
        VerifiedPuzzle(
            definition=puzzle,
            solution=result.first_solution,
            stats=result.stats,
        ),
        result,
    )
