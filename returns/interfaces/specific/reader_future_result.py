from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, TypeVar, final

from returns.interfaces.specific import future_result, reader, reader_ioresult
from returns.primitives.asserts import assert_equal
from returns.primitives.laws import (
    Law2,
    Lawful,
    LawSpecDef,
    law_definition,
)

if TYPE_CHECKING:
    pass
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_ValueType = TypeVar('_ValueType')
_ErrorType = TypeVar('_ErrorType')
_EnvType = TypeVar('_EnvType')
_ReaderFutureResultLikeType = TypeVar(
    '_ReaderFutureResultLikeType', bound='ReaderFutureResultLikeN'
)


class ReaderFutureResultLikeN(
    reader_ioresult.ReaderIOResultLikeN[_FirstType, _SecondType, _ThirdType],
    future_result.FutureResultLikeN[_FirstType, _SecondType, _ThirdType],
):
    """
    Interface for all types that do look like ``ReaderFutureResult`` instance.

    Cannot be called.
    """

    __slots__ = ()

    @abstractmethod
    def bind_context_future_result(self, function):
        """Bind a ``ReaderFutureResult`` returning function over a container."""

    @abstractmethod
    def bind_async_context_future_result(self, function):
        """Bind async ``ReaderFutureResult`` function."""

    @classmethod
    @abstractmethod
    def from_future_result_context(cls, inner_value):
        """Unit method to create new containers from ``ReaderFutureResult``."""


ReaderFutureResultLike3 = ReaderFutureResultLikeN[
    _FirstType, _SecondType, _ThirdType
]


@final
class _LawSpec(LawSpecDef):
    """
    Concrete laws for ``ReaderFutureResultBasedN``.

    See: https://github.com/haskell/mtl/pull/61/files
    """

    __slots__ = ()

    @law_definition
    def asking_law(container, env):
        """Asking for an env, always returns the env."""
        assert_equal(
            container.ask().__call__(env),
            container.from_value(env).__call__(env),
        )


class ReaderFutureResultBasedN(
    ReaderFutureResultLikeN[_FirstType, _SecondType, _ThirdType],
    reader.CallableReader3[
        _FirstType,
        _SecondType,
        _ThirdType,
        'FutureResult[_FirstType, _SecondType]',
        _ThirdType,
    ],
    Lawful['ReaderFutureResultBasedN[_FirstType, _SecondType, _ThirdType]'],
):
    """
    This interface is very specific to our ``ReaderFutureResult`` type.

    The only thing that differs from ``ReaderFutureResultLikeN``
    is that we know the specific types for its ``__call__`` method.

    In this case the return type of ``__call__`` is ``FutureResult``.
    """

    __slots__ = ()
    _laws = (Law2(_LawSpec.asking_law),)


ReaderFutureResultBased3 = ReaderFutureResultBasedN[
    _FirstType, _SecondType, _ThirdType
]
