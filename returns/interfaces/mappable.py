from abc import abstractmethod
from typing import Generic, Never, TypeVar, final

from returns.functions import compose, identity
from returns.primitives.asserts import assert_equal
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
_MappableType = TypeVar('_MappableType', bound='MappableN')
_NewType1 = TypeVar('_NewType1')
_NewType2 = TypeVar('_NewType2')


@final
class _LawSpec(LawSpecDef):
    """
    Mappable or functor laws.

    https://en.wikibooks.org/wiki/Haskell/The_Functor_class#The_functor_laws
    """

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


class MappableN(
    Lawful['MappableN[_FirstType, _SecondType, _ThirdType]'],
    Generic[_FirstType, _SecondType, _ThirdType],
):
    """
    Allows to chain wrapped values in containers with regular functions.

    Behaves like a functor.

    See also:
        - https://en.wikipedia.org/wiki/Functor

    """

    __slots__ = ()
    _laws = (Law1(_LawSpec.identity_law), Law3(_LawSpec.associative_law))

    @abstractmethod
    def map(self, function):
        """Allows to run a pure function over a container."""


Mappable1 = MappableN[_FirstType, Never, Never]
Mappable2 = MappableN[_FirstType, _SecondType, Never]
Mappable3 = MappableN[_FirstType, _SecondType, _ThirdType]
