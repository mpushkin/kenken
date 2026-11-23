"""Small deterministic random primitives owned by generator v0.1."""

from __future__ import annotations

from collections.abc import MutableSequence
from typing import TypeVar

_T = TypeVar("_T")
_MASK = 2**64 - 1


class RandomV1:
    """SplitMix64-based stream whose output is independent of Python's random module."""

    def __init__(self, seed: int) -> None:
        if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed <= _MASK:
            raise ValueError("seed must be a uint64")
        self._state = seed

    def _next(self) -> int:
        self._state = (self._state + 0x9E3779B97F4A7C15) & _MASK
        value = self._state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & _MASK
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & _MASK
        return value ^ (value >> 31)

    def randbelow(self, stop: int) -> int:
        if stop <= 0:
            raise ValueError("stop must be positive")
        limit = 2**64 - (2**64 % stop)
        while True:
            value = self._next()
            if value < limit:
                return value % stop

    def choice(self, values: list[_T] | tuple[_T, ...]) -> _T:
        if not values:
            raise ValueError("cannot choose from an empty sequence")
        return values[self.randbelow(len(values))]

    def shuffle(self, values: MutableSequence[_T]) -> None:
        for index in range(len(values) - 1, 0, -1):
            other = self.randbelow(index + 1)
            values[index], values[other] = values[other], values[index]
