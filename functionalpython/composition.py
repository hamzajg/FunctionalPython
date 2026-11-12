"""Composing and currying functions."""

from __future__ import annotations

import inspect
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose right to left: ``compose(f, g)(x) == f(g(x))``.

    ``compose()`` is the identity function.
    """
    if not functions:
        return lambda value: value

    def composed(value: Any) -> Any:
        for function in reversed(functions):
            value = function(value)
        return value

    return composed


def pipe(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose left to right: ``pipe(f, g)(x) == g(f(x))``.

    ``pipe()`` is the identity function.
    """
    if not functions:
        return lambda value: value

    def piped(value: Any) -> Any:
        for function in functions:
            value = function(value)
        return value

    return piped


def curry(function: Callable[..., T]) -> Callable[..., Any]:
    """Curry a function so it can be called in several steps.

    ``curry(add)(1)(2) == curry(add)(1, 2) == add(1, 2)``.

    Only required positional parameters are counted. Keyword arguments are not
    supported by the curried form.
    """
    required = [
        parameter
        for parameter in inspect.signature(function).parameters.values()
        if parameter.kind
        in (parameter.POSITIONAL_ONLY, parameter.POSITIONAL_OR_KEYWORD)
        and parameter.default is parameter.empty
    ]
    arity = len(required)

    if arity == 0:
        return function

    def build(collected: tuple) -> Callable[..., Any]:
        def curried(*args: Any) -> Any:
            combined = collected + args
            if len(combined) > arity:
                raise TypeError(
                    f"{function.__name__}() takes {arity} positional arguments "
                    f"but {len(combined)} were given"
                )
            if len(combined) == arity:
                return function(*combined)
            return build(combined)

        return curried

    return build(())
