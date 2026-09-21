from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from returns.interfaces.specific.reader_ioresult import ReaderIOResultLikeN
from returns.primitives.hkt import kinded

if TYPE_CHECKING:
    pass
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_ReaderIOResultLikeKind = TypeVar(
    '_ReaderIOResultLikeKind', bound=ReaderIOResultLikeN
)


def bind_context_ioresult(function):
    """
    Lifts function from ``RequiresContextIOResult`` for better composition.

    In other words, it modifies the function's
    signature from:
    ``a -> RequiresContextIOResult[env, b, c]``
    to:
    ``Container[env, a, c]`` -> ``Container[env, b, c]``

    .. code:: python

      >>> import anyio
      >>> from returns.context import (
      ...     RequiresContextFutureResult,
      ...     RequiresContextIOResult,
      ... )
      >>> from returns.io import IOSuccess, IOFailure
      >>> from returns.pointfree import bind_context_ioresult

      >>> def function(arg: int) -> RequiresContextIOResult[str, int, str]:
      ...     return RequiresContextIOResult(
      ...         lambda deps: IOSuccess(len(deps) + arg),
      ...     )

      >>> assert anyio.run(bind_context_ioresult(function)(
      ...     RequiresContextFutureResult.from_value(2),
      ... )('abc').awaitable) == IOSuccess(5)
      >>> assert anyio.run(bind_context_ioresult(function)(
      ...     RequiresContextFutureResult.from_failure(0),
      ... )('abc').awaitable) == IOFailure(0)

    """

    @kinded
    def factory(container):
        return container.bind_context_ioresult(function)

    return factory
