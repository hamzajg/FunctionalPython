"""Lazy sequences built from generators and ``itertools``."""

from __future__ import annotations

from itertools import count, islice
from typing import Iterable, Iterator, List, TypeVar

T = TypeVar("T")


def naturals(start: int = 0) -> Iterator[int]:
    """An infinite stream of integers starting at ``start``."""
    return count(start)


def take(count_: int, iterable: Iterable[T]) -> List[T]:
    """Materialise at most ``count_`` items from an iterable."""
    if count_ < 0:
        raise ValueError("count_ must be non-negative")
    return list(islice(iterable, count_))


def fibonacci() -> Iterator[int]:
    """An infinite Fibonacci stream: 0, 1, 1, 2, 3, ..."""
    current, following = 0, 1
    while True:
        yield current
        current, following = following, current + following


def chunks(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield lists of at most ``size`` items, lazily.

    The last chunk may be shorter. Nothing is read until the consumer asks
    for the next chunk.
    """
    if size <= 0:
        raise ValueError("size must be positive")

    buffer: List[T] = []
    for item in iterable:
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []
    if buffer:
        yield buffer


def unique_seen(iterable: Iterable[T]) -> Iterator[T]:
    """Yield each value once, remembering what has been seen."""
    seen: set = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item
