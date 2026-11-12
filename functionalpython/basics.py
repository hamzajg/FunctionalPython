"""Pure functions over sequences.

Every function here returns a new object and never mutates its input.
"""

from __future__ import annotations

from typing import Callable, Iterable, List, Sequence, TypeVar

T = TypeVar("T")
K = TypeVar("K")


def square_all(numbers: Iterable[float]) -> List[float]:
    """Return a new list with every number squared."""
    return [number * number for number in numbers]


def evens(numbers: Iterable[int]) -> List[int]:
    """Return the even numbers, in order."""
    return [number for number in numbers if number % 2 == 0]


def total(numbers: Iterable[float]) -> float:
    """Sum an iterable. Empty input sums to 0."""
    return sum(numbers)


def dedupe(items: Iterable[T]) -> List[T]:
    """Remove duplicates while preserving first-seen order.

    Unlike ``set(items)`` this keeps the input order and works with
    unhashable values.
    """
    result: List[T] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def sort_by(
    items: Iterable[T], key: Callable[[T], K], reverse: bool = False
) -> List[T]:
    """Return a new list sorted by ``key``.

    ``sorted`` is stable, so equal keys keep their input order.
    """
    return sorted(items, key=key, reverse=reverse)


def pairs(left: Sequence[T], right: Sequence[T]) -> List[tuple]:
    """Zip two sequences into a list of tuples (strict about length)."""
    if len(left) != len(right):
        raise ValueError(
            f"sequences must have the same length, got {len(left)} and {len(right)}"
        )
    return list(zip(left, right))
