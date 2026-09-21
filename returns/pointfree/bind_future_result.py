from typing import TypeVar

from returns.interfaces.specific.future_result import FutureResultLikeN
from returns.primitives.hkt import kinded

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_FutureResultKind = TypeVar('_FutureResultKind', bound=FutureResultLikeN)


def bind_future_result(function):
    """
    Compose a container and async function returning ``FutureResult``.

    In other words, it modifies the function
    signature from:
    ``a -> FutureResult[b, c]``
    to:
    ``Container[a, c] -> Container[b, c]``

    This is how it should be used:

    .. code:: python

      >>> import anyio
      >>> from returns.pointfree import bind_future_result
      >>> from returns.future import FutureResult
      >>> from returns.io import IOSuccess, IOFailure

      >>> def example(argument: int) -> FutureResult[int, str]:
      ...     return FutureResult.from_value(argument + 1)

      >>> assert anyio.run(
      ...     bind_future_result(example)(
      ...         FutureResult.from_value(1),
      ...     ).awaitable,
      ... ) == IOSuccess(2)

      >>> assert anyio.run(
      ...     bind_future_result(example)(
      ...         FutureResult.from_failure('a'),
      ...     ).awaitable,
      ... ) == IOFailure('a')

    .. currentmodule: returns.primitives.interfaces.specific.future_result

    Note, that this function works
    for all containers with ``.bind_async_future`` method.
    See :class:`~FutureResultLikeN` for more info.

    """

    @kinded
    def factory(container):
        return container.bind_future_result(function)

    return factory
