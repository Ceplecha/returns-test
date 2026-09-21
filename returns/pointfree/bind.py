from typing import TypeVar

from returns.interfaces.bindable import BindableN
from returns.primitives.hkt import kinded

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_BindableKind = TypeVar('_BindableKind', bound=BindableN)


def bind(function):
    """
    Turns function's input parameter from a regular value to a container.

    In other words, it modifies the function
    signature from:
    ``a -> Container[b]``
    to:
    ``Container[a] -> Container[b]``

    Similar to :func:`returns.pointfree.lash`,
    but works for successful containers.
    This is how it should be used:

    .. code:: python

      >>> from returns.pointfree import bind
      >>> from returns.maybe import Maybe, Some, Nothing

      >>> def example(argument: int) -> Maybe[int]:
      ...     return Some(argument + 1)

      >>> assert bind(example)(Some(1)) == Some(2)
      >>> assert bind(example)(Nothing) == Nothing

    Note, that this function works for all containers with ``.bind`` method.
    See :class:`returns.primitives.interfaces.bindable.BindableN` for more info.

    """

    @kinded
    def factory(container):
        return container.bind(function)

    return factory
