from typing import TypeVar

from returns.interfaces.specific.ioresult import IOResultLikeN
from returns.primitives.hkt import kinded

_FirstType = TypeVar('_FirstType')
_NewFirstType = TypeVar('_NewFirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_IOResultLikeKind = TypeVar('_IOResultLikeKind', bound=IOResultLikeN)


def compose_result(function):
    """
    Composes inner ``Result`` with ``IOResultLike`` returning function.

    Can be useful when you need an access to both states of the result.

    .. code:: python

      >>> from returns.io import IOResult, IOSuccess, IOFailure
      >>> from returns.pointfree import compose_result
      >>> from returns.result import Result

      >>> def modify_string(container: Result[str, str]) -> IOResult[str, str]:
      ...     return IOResult.from_result(
      ...         container.map(str.upper).alt(str.lower),
      ...     )

      >>> assert compose_result(modify_string)(
      ...     IOSuccess('success')
      ... ) == IOSuccess('SUCCESS')
      >>> assert compose_result(modify_string)(
      ...     IOFailure('FAILURE')
      ... ) == IOFailure('failure')

    """

    @kinded
    def factory(container):
        return container.compose_result(function)

    return factory
