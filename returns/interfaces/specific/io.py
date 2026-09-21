from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Never, TypeVar

from returns.interfaces import container, equable

if TYPE_CHECKING:
    pass
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_IOLikeType = TypeVar('_IOLikeType', bound='IOLikeN')


class IOLikeN(container.ContainerN[_FirstType, _SecondType, _ThirdType]):
    """
    Represents interface for types that looks like fearless ``IO``.

    This type means that ``IO`` cannot fail. Like random numbers, date, etc.
    Don't use this type for ``IO`` that can. Instead, use
    :class:`returns.interfaces.specific.ioresult.IOResultBasedN` type.

    """

    __slots__ = ()

    @abstractmethod
    def bind_io(self, function):
        """Allows to apply a wrapped function over a container."""

    @classmethod
    @abstractmethod
    def from_io(cls, inner_value):
        """Unit method to create new containers from successful ``IO``."""


IOLike1 = IOLikeN[_FirstType, Never, Never]
IOLike2 = IOLikeN[_FirstType, _SecondType, Never]
IOLike3 = IOLikeN[_FirstType, _SecondType, _ThirdType]


class IOBasedN(IOLikeN[_FirstType, _SecondType, _ThirdType], equable.Equable):
    """
    Represents the base interface for types that do fearless ``IO``.

    This type means that ``IO`` cannot fail. Like random numbers, date, etc.
    Don't use this type for ``IO`` that can. Instead, use
    :class:`returns.interfaces.specific.ioresult.IOResultBasedN` type.

    This interface also supports direct comparison of two values.
    While ``IOLikeN`` is different. It can be lazy and cannot be compared.

    """

    __slots__ = ()


IOBased1 = IOBasedN[_FirstType, Never, Never]
IOBased2 = IOBasedN[_FirstType, _SecondType, Never]
IOBased3 = IOBasedN[_FirstType, _SecondType, _ThirdType]
