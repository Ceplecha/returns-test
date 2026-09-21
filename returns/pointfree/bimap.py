from typing import TypeVar

from returns.interfaces.bimappable import BiMappableN
from returns.primitives.hkt import kinded

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType1 = TypeVar('_UpdatedType1')
_UpdatedType2 = TypeVar('_UpdatedType2')
_BiMappableKind = TypeVar('_BiMappableKind', bound=BiMappableN)


def bimap(on_first, on_second):
    """
    Maps container on both: first and second arguments.

    Can be used to synchronize state on both success and failure.

    This is how it should be used:

    .. code:: python

        >>> from returns.io import IOSuccess, IOFailure
        >>> from returns.pointfree import bimap

        >>> def first(argument: int) -> float:
        ...     return argument / 2

        >>> def second(argument: str) -> bool:
        ...     return bool(argument)

        >>> assert bimap(first, second)(IOSuccess(1)) == IOSuccess(0.5)
        >>> assert bimap(first, second)(IOFailure('')) == IOFailure(False)

    Note, that this function works
    for all containers with ``.map`` and ``.alt`` methods.
    See :class:`returns.primitives.interfaces.bimappable.BiMappableN`
    for more info.

    """

    @kinded
    def factory(container):
        return container.map(on_first).alt(on_second)

    return factory
