"""
Represents the base interfaces for types that do fear-some async operations.

This type means that ``FutureResult`` can (and will!) fail with exceptions.

Use this type to mark that this specific async opetaion can fail.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Never, TypeVar

from returns.interfaces.specific import future, ioresult

if TYPE_CHECKING:
    pass
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_ValueType = TypeVar('_ValueType')
_ErrorType = TypeVar('_ErrorType')
_FutureResultLikeType = TypeVar(
    '_FutureResultLikeType', bound='FutureResultLikeN'
)


class FutureResultLikeN(
    future.FutureLikeN[_FirstType, _SecondType, _ThirdType],
    ioresult.IOResultLikeN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base type for ones that does look like ``FutureResult``.

    But at the time this is not a real ``Future`` and cannot be awaited.
    It is also cannot be unwrapped, because it is not a real ``IOResult``.
    """

    __slots__ = ()

    @abstractmethod
    def bind_future_result(self, function):
        """Allows to bind ``FutureResult`` functions over a container."""

    @abstractmethod
    def bind_async_future_result(self, function):
        """Allows to bind async ``FutureResult`` functions over container."""

    @classmethod
    @abstractmethod
    def from_failed_future(cls, inner_value):
        """Creates new container from a failed ``Future``."""

    @classmethod
    def from_future_result(cls, inner_value):
        """Creates container from ``FutureResult`` instance."""


FutureResultLike2 = FutureResultLikeN[_FirstType, _SecondType, Never]
FutureResultLike3 = FutureResultLikeN[_FirstType, _SecondType, _ThirdType]


class FutureResultBasedN(
    future.FutureBasedN[_FirstType, _SecondType, _ThirdType],
    FutureResultLikeN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base type for real ``FutureResult`` objects.

    They can be awaited.
    Still cannot be unwrapped.
    """

    __slots__ = ()


FutureResultBased2 = FutureResultBasedN[_FirstType, _SecondType, Never]
FutureResultBased3 = FutureResultBasedN[_FirstType, _SecondType, _ThirdType]
