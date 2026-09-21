"""
An interface that represents a pure computation result.

For impure result see
:class:`returns.interfaces.specific.ioresult.IOResultLikeN` type.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Never, TypeVar

from returns.interfaces import equable, failable, unwrappable

if TYPE_CHECKING:
    pass
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_ResultLikeType = TypeVar('_ResultLikeType', bound='ResultLikeN')
_ValueType = TypeVar('_ValueType')
_ErrorType = TypeVar('_ErrorType')
_FirstUnwrappableType = TypeVar('_FirstUnwrappableType')
_SecondUnwrappableType = TypeVar('_SecondUnwrappableType')


class ResultLikeN(
    failable.DiverseFailableN[_FirstType, _SecondType, _ThirdType]
):
    """
    Base types for types that looks like ``Result`` but cannot be unwrapped.

    Like ``RequiresContextResult`` or ``FutureResult``.
    """

    __slots__ = ()

    @abstractmethod
    def bind_result(self, function):
        """Runs ``Result`` returning function over a container."""

    @classmethod
    @abstractmethod
    def from_result(cls, inner_value):
        """Unit method to create new containers from any raw value."""


ResultLike2 = ResultLikeN[_FirstType, _SecondType, Never]
ResultLike3 = ResultLikeN[_FirstType, _SecondType, _ThirdType]


class UnwrappableResult(
    ResultLikeN[_FirstType, _SecondType, _ThirdType],
    unwrappable.Unwrappable[_FirstUnwrappableType, _SecondUnwrappableType],
    equable.Equable,
):
    """
    Intermediate type with 5 type arguments that represents unwrappable result.

    It is a raw type and should not be used directly.
    Use ``ResultBasedN`` and ``IOResultBasedN`` instead.
    """

    __slots__ = ()


class ResultBasedN(
    UnwrappableResult[
        _FirstType, _SecondType, _ThirdType, _FirstType, _SecondType
    ]
):
    """
    Base type for real ``Result`` types.

    Can be unwrapped.
    """

    __slots__ = ()


ResultBased2 = ResultBasedN[_FirstType, _SecondType, Never]
ResultBased3 = ResultBasedN[_FirstType, _SecondType, _ThirdType]
