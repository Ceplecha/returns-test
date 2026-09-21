from abc import abstractmethod
from typing import Never, TypeVar, final

from returns.interfaces import bimappable
from returns.primitives.asserts import assert_equal
from returns.primitives.laws import (
    Law1,
    Lawful,
    LawSpecDef,
    law_definition,
)

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_SwappableType = TypeVar('_SwappableType', bound='SwappableN')


@final
class _LawSpec(LawSpecDef):
    """Laws for :class:`~SwappableN` type."""

    __slots__ = ()

    @law_definition
    def double_swap_law(container):
        """
        Swapping container twice.

        It ensure that we get the initial value back.
        In other words, swapping twice does nothing.
        """
        assert_equal(container, container.swap().swap())


class SwappableN(
    bimappable.BiMappableN[_FirstType, _SecondType, _ThirdType],
    Lawful['SwappableN[_FirstType, _SecondType, _ThirdType]'],
):
    """Interface that allows swapping first and second type values."""

    __slots__ = ()
    _laws = (Law1(_LawSpec.double_swap_law),)

    @abstractmethod
    def swap(self):
        """Swaps first and second types in ``SwappableN``."""


Swappable2 = SwappableN[_FirstType, _SecondType, Never]
Swappable3 = SwappableN[_FirstType, _SecondType, _ThirdType]
