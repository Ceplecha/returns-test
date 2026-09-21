from typing import TypeVar

from returns.interfaces.mappable import MappableN
from returns.primitives.hkt import kinded

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_MappableKind = TypeVar('_MappableKind', bound=MappableN)


def map_(function):
    """
    Lifts function to be wrapped in a container for better composition.

    In other words, it modifies the function's
    signature from:
    ``a -> b``
    to: ``Container[a] -> Container[b]``

    This is how it should be used:

    .. code:: python

        >>> from returns.io import IO
        >>> from returns.pointfree import map_

        >>> def example(argument: int) -> float:
        ...     return argument / 2

        >>> assert map_(example)(IO(1)) == IO(0.5)

    Note, that this function works for all containers with ``.map`` method.
    See :class:`returns.primitives.interfaces.mappable.MappableN` for more info.

    See also:
        - https://wiki.haskell.org/Lifting

    """

    @kinded
    def factory(container):
        return container.map(function)

    return factory
