from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, TypeVar, final

from returns.interfaces.specific import reader, result
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
_ReaderResultLikeType = TypeVar(
    '_ReaderResultLikeType', bound='ReaderResultLikeN'
)


class ReaderResultLikeN(
    reader.ReaderLike3[_FirstType, _SecondType, _ThirdType],
    result.ResultLikeN[_FirstType, _SecondType, _ThirdType],
):
    """
    Base interface for all types that do look like ``ReaderResult`` instance.

    Cannot be called.
    """

    __slots__ = ()

    @abstractmethod
    def bind_context_result(self, function):
        """Binds a ``ReaderResult`` returning function over a container."""

    @classmethod
    @abstractmethod
    def from_failed_context(cls, inner_value):
        """Unit method to create new containers from failed ``Reader``."""

    @classmethod
    @abstractmethod
    def from_result_context(cls, inner_value):
        """Unit method to create new containers from ``ReaderResult``."""


ReaderResultLike3 = ReaderResultLikeN[_FirstType, _SecondType, _ThirdType]


@final
class _LawSpec(LawSpecDef):
    """
    Concrete laws for ``ReaderResultBasedN``.

    See: https://github.com/haskell/mtl/pull/61/files
    """

    __slots__ = ()

    @law_definition
    def purity_law(container, env):
        """Calling a ``Reader`` twice has the same result with the same env."""
        assert container(env) == container(env)

    @law_definition
    def asking_law(container, env):
        """Asking for an env, always returns the env."""
        assert container.ask().__call__(env) == container.from_value(
            env
        ).__call__(env)


class ReaderResultBasedN(
    ReaderResultLikeN[_FirstType, _SecondType, _ThirdType],
    reader.CallableReader3[
        _FirstType,
        _SecondType,
        _ThirdType,
        'Result[_FirstType, _SecondType]',
        _ThirdType,
    ],
    Lawful['ReaderResultBasedN[_FirstType, _SecondType, _ThirdType]'],
):
    """
    This interface is very specific to our ``ReaderResult`` type.

    The only thing that differs from ``ReaderResultLikeN`` is that we know
    the specific types for its ``__call__`` method.

    In this case the return type of ``__call__`` is ``Result``.
    """

    __slots__ = ()
    _laws = (Law2(_LawSpec.purity_law), Law2(_LawSpec.asking_law))


ReaderResultBased3 = ReaderResultBasedN[_FirstType, _SecondType, _ThirdType]
