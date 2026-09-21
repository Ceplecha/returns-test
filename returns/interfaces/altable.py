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
_AltableType = TypeVar('_AltableType', bound='AltableN')
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
    def identity_law(altable):
        """Mapping identity over a value must return the value unchanged."""
        assert_equal(altable.alt(identity), altable)

    @law_definition
    def associative_law(altable, first, second):
        """Mapping twice or mapping a composition is the same thing."""
        assert_equal(
            altable.alt(first).alt(second), altable.alt(compose(first, second))
        )


class AltableN(
    Lawful['AltableN[_FirstType, _SecondType, _ThirdType]'],
    Generic[_FirstType, _SecondType, _ThirdType],
):
    """Modifies the second type argument with a pure function."""

    __slots__ = ()
    _laws = (Law1(_LawSpec.identity_law), Law3(_LawSpec.associative_law))

    @abstractmethod
    def alt(self, function):
        """Allows to run a pure function over a container."""


Altable2 = AltableN[_FirstType, _SecondType, Never]
Altable3 = AltableN[_FirstType, _SecondType, _ThirdType]
