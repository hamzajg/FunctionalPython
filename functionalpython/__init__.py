"""Small, tested examples of functional programming in Python.

The package is intentionally dependency-free: everything here uses the standard
library so the examples stay runnable anywhere.
"""

from .basics import dedupe, evens, sort_by, square_all, total
from .composition import compose, curry, pipe
from .higher_order import (
    apply_twice,
    filter_all,
    make_multiplier,
    map_all,
    partial_apply,
    reduce_all,
)
from .lazy import chunks, fibonacci, naturals, take, unique_seen
from .maybe import Just, Maybe, Nothing
from .recursion import factorial, memoize, trampoline

__all__ = [
    "Just",
    "Maybe",
    "Nothing",
    "apply_twice",
    "chunks",
    "compose",
    "curry",
    "dedupe",
    "evens",
    "factorial",
    "fibonacci",
    "filter_all",
    "make_multiplier",
    "map_all",
    "memoize",
    "naturals",
    "partial_apply",
    "pipe",
    "reduce_all",
    "sort_by",
    "square_all",
    "take",
    "total",
    "trampoline",
    "unique_seen",
]
