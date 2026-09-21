"""
An interface for types that do ``IO`` and can fail.

It is a base interface for both sync and async ``IO`` stacks.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Never, TypeVar

from returns.interfaces.specific import io, result

if TYPE_CHECKING:
    pass
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_ValueType = TypeVar('_ValueType')
_ErrorType = TypeVar('_ErrorType')
_IOResultLikeType = TypeVar('_IOResultLikeType', bound='IOResultLikeN')


class IOResultLikeN(
    io.IOLikeN[_FirstType, _SecondType, _ThirdType],
    result.ResultLikeN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base type for types that look like ``IOResult`` but cannot be unwrapped.

    Like ``FutureResult`` or ``RequiresContextIOResult``.
    """

    __slots__ = ()

    @abstractmethod
    def bind_ioresult(self, function):
        """Runs ``IOResult`` returning function over a container."""

    @abstractmethod
    def compose_result(self, function):
        """Allows to compose the underlying ``Result`` with a function."""

    @classmethod
    @abstractmethod
    def from_ioresult(cls, inner_value):
        """Unit method to create new containers from ``IOResult`` type."""

    @classmethod
    @abstractmethod
    def from_failed_io(cls, inner_value):
        """Unit method to create new containers from failed ``IO``."""


IOResultLike2 = IOResultLikeN[_FirstType, _SecondType, Never]
IOResultLike3 = IOResultLikeN[_FirstType, _SecondType, _ThirdType]


class IOResultBasedN(
    IOResultLikeN[_FirstType, _SecondType, _ThirdType],
    io.IOBasedN[_FirstType, _SecondType, _ThirdType],
    result.UnwrappableResult[
        _FirstType, _SecondType, _ThirdType, 'IO[_FirstType]', 'IO[_SecondType]'
    ],
):
    """
    Base type for real ``IOResult`` types.

    Can be unwrapped.
    """

    __slots__ = ()


IOResultBased2 = IOResultBasedN[_FirstType, _SecondType, Never]
IOResultBased3 = IOResultBasedN[_FirstType, _SecondType, _ThirdType]
