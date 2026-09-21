from typing import TypeVar

from returns.contrib.hypothesis.laws import check_all_laws
from returns.interfaces import applicative
from returns.primitives.container import BaseContainer
from returns.primitives.hkt import SupportsKind1

_ValueType = TypeVar('_ValueType')
_NewValueType = TypeVar('_NewValueType')


class _Wrapper(
    BaseContainer,
    SupportsKind1['_Wrapper', _ValueType],
    applicative.Applicative1[_ValueType],
):
    def __init__(self, inner_value):
        super().__init__(inner_value)

    def map(self, function):
        return _Wrapper(function(self._inner_value))

    def apply(self, container):
        function = container._inner_value
        return _Wrapper(function(self._inner_value))

    @classmethod
    def from_value(cls, inner_value):
        return _Wrapper(inner_value)


check_all_laws(_Wrapper)
