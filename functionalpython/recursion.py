"""Recursion, memoisation, and trampolining."""

from __future__ import annotations

import threading
from functools import wraps
from typing import Any, Callable, Dict, Tuple


def factorial(number: int) -> int:
    """Recursive factorial. Rejects negative input."""
    if number < 0:
        raise ValueError("number must be non-negative")
    if number in (0, 1):
        return 1
    return number * factorial(number - 1)


def memoize(function: Callable[..., Any]) -> Callable[..., Any]:
    """Cache results by positional arguments.

    The wrapped function must be called with hashable positional arguments.
    """
    cache: Dict[Tuple[Any, ...], Any] = {}

    @wraps(function)
    def wrapper(*args: Any) -> Any:
        if args not in cache:
            cache[args] = function(*args)
        return cache[args]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper


# Tracks whether the current thread is already inside a trampoline loop, so a
# recursive call made from a thunk hands its result back to that loop instead
# of starting a nested one.
_running = threading.local()


def trampoline(function: Callable[..., Any]) -> Callable[..., Any]:
    """Turn a function returning thunks into a loop.

    A recursive function written to return ``lambda: recursive_call(...)``
    instead of calling itself avoids growing the Python stack: the decorator
    keeps calling the returned thunks in a loop until one returns a value.

    The decorated name can be called recursively from inside a thunk. Such a
    call returns its result (often another thunk) to the loop that is already
    running instead of starting a second, nested loop, so the stack stays flat.

    Because every callable result is treated as a thunk, a function decorated
    with ``trampoline`` must not return a callable as its final value.
    """

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        depth = getattr(_running, "depth", 0)
        _running.depth = depth + 1
        try:
            result = function(*args, **kwargs)

            if depth:
                # Called from inside a running loop (a recursive thunk): the
                # outer loop will unwrap this result, so do not loop here.
                return result

            while callable(result):
                result = result()
            return result
        finally:
            _running.depth = depth

    return wrapper
