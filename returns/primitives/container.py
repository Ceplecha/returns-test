from abc import ABC
from typing import Any, TypeVar

from typing_extensions import TypedDict

from returns.interfaces.equable import Equable
from returns.primitives.types import Immutable

_EqualType = TypeVar('_EqualType', bound=Equable)


class _PickleState(TypedDict):
    """Dict to represent the `BaseContainer` state to be pickled."""

    __slots__ = ('container_value',)
    container_value: Any


class BaseContainer(Immutable, ABC):
    """Utility class to provide all needed magic methods to the context."""

    __slots__ = ('_inner_value',)

    def __init__(self, inner_value):
        """
        Wraps the given value in the Container.

        'value' is any arbitrary value of any type including functions.
        """
        object.__setattr__(self, '_inner_value', inner_value)

    def __repr__(self):
        """Used to display details of object."""
        return '<{}: {}>'.format(
            self.__class__.__qualname__.strip('_'), str(self._inner_value)
        )

    def __eq__(self, other):
        """Used to compare two 'Container' objects."""
        return container_equality(self, other)

    def __hash__(self):
        """Used to use this value as a key."""
        return hash(self._inner_value)

    def __getstate__(self):
        """That's how this object will be pickled."""
        return {'container_value': self._inner_value}

    def __setstate__(self, state):
        """Loading state from pickled data."""
        if isinstance(state, dict) and 'container_value' in state:
            object.__setattr__(self, '_inner_value', state['container_value'])
        else:
            object.__setattr__(self, '_inner_value', state)


def container_equality(self, other):
    """
    Function to compare similar containers.

    Compares both their types and their inner values.
    """
    if type(self) != type(other):
        return False
    return bool(self._inner_value == other._inner_value)
