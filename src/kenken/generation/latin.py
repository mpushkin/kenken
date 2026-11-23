"""Seeded Latin-square construction."""

from __future__ import annotations

from kenken.model import Grid
from kenken.randomness import RandomV1


def latin_grid(size: int, random: RandomV1) -> Grid:
    symbols = list(range(1, size + 1))
    rows = list(range(size))
    columns = list(range(size))
    random.shuffle(symbols)
    random.shuffle(rows)
    random.shuffle(columns)
    return tuple(
        tuple(symbols[(rows[row] + columns[column]) % size] for column in range(size))
        for row in range(size)
    )
