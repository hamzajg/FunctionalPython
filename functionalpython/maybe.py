"""A small Maybe monad for optional values."""

from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Maybe(Generic[T]):
    """Base class for ``Just(value)`` and ``Nothing()``.

    Subclasses implement ``map``, ``bind``, and ``get_or_else``.
    """

    def map(self, function: Callable[[T], U]) -> "Maybe[U]":
        raise NotImplementedError

    def bind(self, function: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        raise NotImplementedError

    def get_or_else(self, default: U) -> Any:
        raise NotImplementedError

    def is_just(self) -> bool:
        raise NotImplementedError


class Just(Maybe[T]):
    """A present value."""

    def __init__(self, value: T) -> None:
        self.value = value

    def map(self, function: Callable[[T], U]) -> "Maybe[U]":
        return Just(function(self.value))

    def bind(self, function: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        result = function(self.value)
        if not isinstance(result, Maybe):
            raise TypeError("bind() callable must return a Maybe")
        return result

    def get_or_else(self, default: U) -> T:
        return self.value

    def is_just(self) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Just) and other.value == self.value

    def __repr__(self) -> str:
        return f"Just({self.value!r})"


class Nothing(Maybe[T]):
    """An absent value."""

    def map(self, function: Callable[[T], U]) -> "Maybe[U]":
        return Nothing()

    def bind(self, function: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        return Nothing()

    def get_or_else(self, default: U) -> U:
        return default

    def is_just(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Nothing)

    def __repr__(self) -> str:
        return "Nothing()"
