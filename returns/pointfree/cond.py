from typing import TypeVar, overload

from returns.interfaces.failable import DiverseFailableN, SingleFailableN
from returns.methods.cond import internal_cond

_ValueType = TypeVar('_ValueType')
_ErrorType = TypeVar('_ErrorType')
_DiverseFailableKind = TypeVar('_DiverseFailableKind', bound=DiverseFailableN)
_SingleFailableKind = TypeVar('_SingleFailableKind', bound=SingleFailableN)


@overload
def cond(container_type, success_value): ...


@overload
def cond(container_type, success_value, error_value): ...


def cond(container_type, success_value, error_value=None):
    """
    Reduce the boilerplate when choosing paths.

    Works with ``SingleFailableN`` (e.g. ``Maybe``)
    and ``DiverseFailableN`` (e.g. ``Result``).

    Example using ``cond`` with the ``Result`` container:

    .. code:: python

      >>> from returns.pointfree import cond
      >>> from returns.result import Failure, Result, Success

      >>> assert cond(Result, 'success', 'failure')(True) == Success('success')
      >>> assert cond(Result, 'success', 'failure')(False) == Failure('failure')

    Example using ``cond`` with the ``Maybe`` container:

    .. code:: python

      >>> from returns.maybe import Maybe, Some, Nothing

      >>> assert cond(Maybe, 10.0)(True) == Some(10.0)
      >>> assert cond(Maybe, 10.0)(False) == Nothing

    """

    def factory(is_success):
        return internal_cond(
            container_type, is_success, success_value, error_value
        )

    return factory
