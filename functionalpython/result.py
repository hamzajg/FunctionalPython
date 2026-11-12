"""A small Result monad for error handling without exceptions."""

from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

from .maybe import Just, Maybe, Nothing

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")


class Result(Generic[T, E]):
    """Base class for ``Ok(value)`` and ``Err(error)``.

    A ``Result`` is either a success carrying a value or a failure carrying an
    error, and both cases travel through the same ``map``/``bind`` chain. That
    turns error handling into a value instead of a control-flow jump: a
    failure short-circuits the rest of the chain, like an exception, but the
    caller has to look at it to get the value out.
    """

    def map(self, function: Callable[[T], U]) -> "Result[U, E]":
        raise NotImplementedError

    def map_err(self, function: Callable[[E], F]) -> "Result[T, F]":
        raise NotImplementedError

    def bind(self, function: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        raise NotImplementedError

    def get_or_else(self, default: U) -> Any:
        raise NotImplementedError

    def unwrap(self) -> T:
        raise NotImplementedError

    def unwrap_err(self) -> E:
        raise NotImplementedError

    def ok(self) -> Maybe[T]:
        raise NotImplementedError

    def err(self) -> Maybe[E]:
        raise NotImplementedError

    def is_ok(self) -> bool:
        raise NotImplementedError

    def is_err(self) -> bool:
        raise NotImplementedError


class Ok(Result[T, E]):
    """A successful computation holding a value."""

    def __init__(self, value: T) -> None:
        self.value = value

    def map(self, function: Callable[[T], U]) -> "Result[U, E]":
        return Ok(function(self.value))

    def map_err(self, function: Callable[[E], F]) -> "Result[T, F]":
        return Ok(self.value)

    def bind(self, function: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        result = function(self.value)
        if not isinstance(result, Result):
            raise TypeError("bind() callable must return a Result")
        return result

    def get_or_else(self, default: U) -> T:
        return self.value

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> E:
        raise ValueError(f"called unwrap_err() on Ok: {self.value!r}")

    def ok(self) -> Maybe[T]:
        return Just(self.value)

    def err(self) -> Maybe[E]:
        return Nothing()

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ok) and other.value == self.value

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"


class Err(Result[T, E]):
    """A failed computation holding an error."""

    def __init__(self, error: E) -> None:
        self.error = error

    def map(self, function: Callable[[T], U]) -> "Result[U, E]":
        return Err(self.error)

    def map_err(self, function: Callable[[E], F]) -> "Result[T, F]":
        return Err(function(self.error))

    def bind(self, function: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return Err(self.error)

    def get_or_else(self, default: U) -> U:
        return default

    def unwrap(self) -> T:
        raise ValueError(f"called unwrap() on Err: {self.error!r}")

    def unwrap_err(self) -> E:
        return self.error

    def ok(self) -> Maybe[T]:
        return Nothing()

    def err(self) -> Maybe[E]:
        return Just(self.error)

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Err) and other.error == self.error

    def __repr__(self) -> str:
        return f"Err({self.error!r})"


def safe(function: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
    """Decorator converting an exception-raising function into a Result-returning one."""
    def wrapper(*args: Any, **kwargs: Any) -> Result[T, Exception]:
        try:
            return Ok(function(*args, **kwargs))
        except Exception as ex:
            return Err(ex)
    return wrapper
