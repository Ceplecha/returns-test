"""
Represents the base interfaces for types that do fearless async operations.

This type means that ``Future`` cannot fail.
Don't use this type for async that can. Instead, use
:class:`returns.interfaces.specific.future_result.FutureResultBasedN` type.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, Never, TypeVar

from returns.interfaces.specific import io

if TYPE_CHECKING:
    pass
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_FutureLikeType = TypeVar('_FutureLikeType', bound='FutureLikeN')
_AsyncFutureType = TypeVar('_AsyncFutureType', bound='AwaitableFutureN')


class FutureLikeN(io.IOLikeN[_FirstType, _SecondType, _ThirdType]):
    """
    Base type for ones that does look like ``Future``.

    But at the time this is not a real ``Future`` and cannot be awaited.
    """

    __slots__ = ()

    @abstractmethod
    def bind_future(self, function):
        """Allows to bind ``Future`` returning function over a container."""

    @abstractmethod
    def bind_async_future(self, function):
        """Allows to bind async ``Future`` returning function over container."""

    @abstractmethod
    def bind_async(self, function):
        """Binds async function returning the same type of container."""

    @abstractmethod
    def bind_awaitable(self, function):
        """Allows to bind async function over container."""

    @classmethod
    @abstractmethod
    def from_future(cls, inner_value):
        """Unit method to create new containers from successful ``Future``."""


FutureLike1 = FutureLikeN[_FirstType, Never, Never]
FutureLike2 = FutureLikeN[_FirstType, _SecondType, Never]
FutureLike3 = FutureLikeN[_FirstType, _SecondType, _ThirdType]


class AwaitableFutureN(Generic[_FirstType, _SecondType, _ThirdType]):
    """
    Type that provides the required API for ``Future`` to be async.

    Should not be used directly. Use ``FutureBasedN`` instead.
    """

    __slots__ = ()

    @abstractmethod
    def __await__(self):
        """Magic method to allow ``await`` expression."""

    @abstractmethod
    async def awaitable(self):
        """Underling logic under ``await`` expression."""


AsyncFuture1 = AwaitableFutureN[_FirstType, Never, Never]
AsyncFuture2 = AwaitableFutureN[_FirstType, _SecondType, Never]
AsyncFuture3 = AwaitableFutureN[_FirstType, _SecondType, _ThirdType]


class FutureBasedN(
    FutureLikeN[_FirstType, _SecondType, _ThirdType],
    AwaitableFutureN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base type for real ``Future`` objects.

    They can be awaited.
    """

    __slots__ = ()


FutureBased1 = FutureBasedN[_FirstType, Never, Never]
FutureBased2 = FutureBasedN[_FirstType, _SecondType, Never]
FutureBased3 = FutureBasedN[_FirstType, _SecondType, _ThirdType]
