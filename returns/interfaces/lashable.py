from abc import abstractmethod
from typing import Generic, Never, TypeVar

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_LashableType = TypeVar('_LashableType', bound='LashableN')


class LashableN(Generic[_FirstType, _SecondType, _ThirdType]):
    """
    Represents a "context" in which calculations can be executed.

    ``Rescueable`` allows you to bind together
    a series of calculations while maintaining
    the context of that specific container.

    In contrast to :class:`returns.interfaces.bindable.BinbdaleN`,
    works with the second type value.
    """

    __slots__ = ()

    @abstractmethod
    def lash(self, function):
        """
        Applies 'function' to the result of a previous calculation.

        And returns a new container.
        """


Lashable2 = LashableN[_FirstType, _SecondType, Never]
Lashable3 = LashableN[_FirstType, _SecondType, _ThirdType]
