from abc import abstractmethod
from typing import Generic, Never, TypeVar

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_BindableType = TypeVar('_BindableType', bound='BindableN')


class BindableN(Generic[_FirstType, _SecondType, _ThirdType]):
    """
    Represents a "context" in which calculations can be executed.

    ``Bindable`` allows you to bind together
    a series of calculations while maintaining
    the context of that specific container.

    In contrast to :class:`returns.interfaces.lashable.LashableN`,
    works with the first type argument.
    """

    __slots__ = ()

    @abstractmethod
    def bind(self, function):
        """
        Applies 'function' to the result of a previous calculation.

        And returns a new container.
        """


Bindable1 = BindableN[_FirstType, Never, Never]
Bindable2 = BindableN[_FirstType, _SecondType, Never]
Bindable3 = BindableN[_FirstType, _SecondType, _ThirdType]
