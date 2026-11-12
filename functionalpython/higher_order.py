"""Functions that take or return other functions."""

from __future__ import annotations

from functools import partial, reduce
from typing import Callable, Iterable, List, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def apply_twice(function: Callable[[T], T], value: T) -> T:
    """Apply ``function`` to ``value`` twice: ``f(f(x))``."""
    return function(function(value))


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a function that multiplies its argument by ``factor``.

    The returned function closes over ``factor``.
    """
    if not isinstance(factor, int):
        raise TypeError("factor must be an int")

    def multiply(value: int) -> int:
        return value * factor

    return multiply


def map_all(function: Callable[[T], U], iterable: Iterable[T]) -> List[U]:
    """Eager ``map`` that returns a list."""
    return [function(item) for item in iterable]


def filter_all(predicate: Callable[[T], bool], iterable: Iterable[T]) -> List[T]:
    """Eager ``filter`` that returns a list."""
    return [item for item in iterable if predicate(item)]


def reduce_all(
    function: Callable[[U, T], U], iterable: Iterable[T], initial: U
) -> U:
    """Left fold with an explicit initial value."""
    return reduce(function, iterable, initial)


def partial_apply(
    function: Callable[..., U], *args: object, **kwargs: object
) -> Callable[..., U]:
    """Bind some arguments up front, returning a new function."""
    return partial(function, *args, **kwargs)
