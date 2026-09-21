from typing import TypeVar

from returns.interfaces.specific.maybe import MaybeLikeN
from returns.primitives.hkt import kinded

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_MaybeLikeKind = TypeVar('_MaybeLikeKind', bound=MaybeLikeN)


def bind_optional(function):
    """
    Binds a function returning optional value over a container.

    In other words, it modifies the function's
    signature from:
    ``a -> Optional[b]``
    to:
    ``Container[a] -> Container[b]``

    .. code:: python

      >>> from typing import Optional
      >>> from returns.pointfree import bind_optional
      >>> from returns.maybe import Some, Nothing

      >>> def example(argument: int) -> Optional[int]:
      ...     return argument + 1 if argument > 0 else None

      >>> assert bind_optional(example)(Some(1)) == Some(2)
      >>> assert bind_optional(example)(Some(0)) == Nothing
      >>> assert bind_optional(example)(Nothing) == Nothing

    Note, that this function works
    for all containers with ``.bind_optional`` method.
    See :class:`returns.primitives.interfaces.specific.maybe._MaybeLikeKind`
    for more info.

    """

    @kinded
    def factory(container):
        return container.bind_optional(function)

    return factory
