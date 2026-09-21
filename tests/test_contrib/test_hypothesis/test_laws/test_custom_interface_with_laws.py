from abc import abstractmethod
from typing import Generic, Never, TypeVar, final

from returns.contrib.hypothesis.laws import check_all_laws
from returns.functions import compose, identity
from returns.primitives.asserts import assert_equal
from returns.primitives.container import BaseContainer
from returns.primitives.hkt import SupportsKind1
from returns.primitives.laws import (
    Law1,
    Law3,
    Lawful,
    LawSpecDef,
    law_definition,
)

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_UpdatedType = TypeVar('_UpdatedType')
_MappableType = TypeVar('_MappableType', bound='_MappableN')
_ValueType = TypeVar('_ValueType')
_NewValueType = TypeVar('_NewValueType')
_NewType1 = TypeVar('_NewType1')
_NewType2 = TypeVar('_NewType2')


@final
class _LawSpec(LawSpecDef):
    """Copy of the functor laws for `MappableN`."""

    __slots__ = ()

    @law_definition
    def identity_law(mappable):
        """Mapping identity over a value must return the value unchanged."""
        assert_equal(mappable.map(identity), mappable)

    @law_definition
    def associative_law(mappable, first, second):
        """Mapping twice or mapping a composition is the same thing."""
        assert_equal(
            mappable.map(first).map(second),
            mappable.map(compose(first, second)),
        )


class _MappableN(
    Lawful['_MappableN[_FirstType, _SecondType, _ThirdType]'],
    Generic[_FirstType, _SecondType, _ThirdType],
):
    """Simple "user-defined" copy of `MappableN`."""

    __slots__ = ()
    _laws = (Law1(_LawSpec.identity_law), Law3(_LawSpec.associative_law))

    @abstractmethod
    def map(self, function):
        """Allows to run a pure function over a container."""


_Mappable1 = _MappableN[_FirstType, Never, Never]


class _ParentWrapper(_Mappable1[_ValueType]):
    """Class that is an ancestor of `_Wrapper` but has no laws."""


class _Wrapper(
    BaseContainer,
    SupportsKind1['_Wrapper', _ValueType],
    _ParentWrapper[_ValueType],
):
    """Simple instance of `_MappableN`."""

    def __init__(self, inner_value):
        super().__init__(inner_value)

    def map(self, function):
        return _Wrapper(function(self._inner_value))


check_all_laws(_Wrapper, use_init=True)
