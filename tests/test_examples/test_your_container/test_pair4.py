from abc import abstractmethod
from typing import Never, TypeVar, final

from returns.contrib.hypothesis.laws import check_all_laws
from returns.interfaces import bindable, equable, lashable, swappable
from returns.primitives.asserts import assert_equal
from returns.primitives.container import BaseContainer, container_equality
from returns.primitives.hkt import SupportsKind2, dekind
from returns.primitives.laws import Law2, Law3, LawSpecDef, law_definition

_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')
_ThirdType = TypeVar('_ThirdType')
_NewFirstType = TypeVar('_NewFirstType')
_NewSecondType = TypeVar('_NewSecondType')
_PairLikeKind = TypeVar('_PairLikeKind', bound='PairLikeN')


class _LawSpec(LawSpecDef):
    @law_definition
    def pair_equality_law(raw_value, container):
        """Ensures that unpaired and paired constructors work fine."""
        assert_equal(
            container.from_unpaired(raw_value),
            container.from_paired(raw_value, raw_value),
        )

    @law_definition
    def pair_left_identity_law(pair, container, function):
        """Ensures that unpaired and paired constructors work fine."""
        assert_equal(
            container.from_paired(*pair).pair(function), function(*pair)
        )


class PairLikeN(
    bindable.BindableN[_FirstType, _SecondType, _ThirdType],
    swappable.SwappableN[_FirstType, _SecondType, _ThirdType],
    lashable.LashableN[_FirstType, _SecondType, _ThirdType],
    equable.Equable,
):
    """Special interface for types that look like a ``Pair``."""

    _laws = (
        Law2(_LawSpec.pair_equality_law),
        Law3(_LawSpec.pair_left_identity_law),
    )

    @abstractmethod
    def pair(self, function):
        """Allows to work with both arguments at the same time."""

    @classmethod
    @abstractmethod
    def from_paired(cls, first, second):
        """Allows to create a PairLikeN from just two values."""

    @classmethod
    @abstractmethod
    def from_unpaired(cls, inner_value):
        """Allows to create a PairLikeN from just a single object."""


PairLike2 = PairLikeN[_FirstType, _SecondType, Never]
PairLike3 = PairLikeN[_FirstType, _SecondType, _ThirdType]


@final
class Pair(
    BaseContainer,
    SupportsKind2['Pair', _FirstType, _SecondType],
    PairLike2[_FirstType, _SecondType],
):
    """
    A type that represents a pair of something.

    Like to coordinates ``(x, y)`` or two best friends.
    Or a question and an answer.

    """

    def __init__(self, inner_value):
        """Saves passed tuple as ``._inner_value`` inside this instance."""
        super().__init__(inner_value)

    equals = container_equality

    def map(self, function):
        """
        Changes the first type with a pure function.

        >>> assert Pair((1, 2)).map(str) == Pair(('1', 2))

        """
        return Pair((function(self._inner_value[0]), self._inner_value[1]))

    def bind(self, function):
        """
        Changes the first type with a function returning another ``Pair``.

        >>> def bindable(first: int) -> Pair[str, str]:
        ...     return Pair((str(first), ''))

        >>> assert Pair((1, 'b')).bind(bindable) == Pair(('1', ''))

        """
        return dekind(function(self._inner_value[0]))

    def alt(self, function):
        """
        Changes the second type with a pure function.

        >>> assert Pair((1, 2)).alt(str) == Pair((1, '2'))

        """
        return Pair((self._inner_value[0], function(self._inner_value[1])))

    def lash(self, function):
        """
        Changes the second type with a function returning ``Pair``.

        >>> def lashable(second: int) -> Pair[str, str]:
        ...     return Pair(('', str(second)))

        >>> assert Pair(('a', 2)).lash(lashable) == Pair(('', '2'))

        """
        return dekind(function(self._inner_value[1]))

    def swap(self):
        """
        Swaps ``Pair`` elements.

        >>> assert Pair((1, 2)).swap() == Pair((2, 1))

        """
        return Pair((self._inner_value[1], self._inner_value[0]))

    def pair(self, function):
        """
        Creates a new ``Pair`` from an existing one via a passed function.

        >>> def min_max(first: int, second: int) -> Pair[int, int]:
        ...     return Pair((min(first, second), max(first, second)))

        >>> assert Pair((2, 1)).pair(min_max) == Pair((1, 2))
        >>> assert Pair((1, 2)).pair(min_max) == Pair((1, 2))

        """
        return dekind(function(self._inner_value[0], self._inner_value[1]))

    @classmethod
    def from_paired(cls, first, second):
        """
        Creates a new pair from two values.

        >>> assert Pair.from_paired(1, 2) == Pair((1, 2))

        """
        return Pair((first, second))

    @classmethod
    def from_unpaired(cls, inner_value):
        """
        Creates a new pair from a single value.

        >>> assert Pair.from_unpaired(1) == Pair((1, 1))

        """
        return Pair((inner_value, inner_value))


check_all_laws(Pair, use_init=True)
