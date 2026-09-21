from typing import TypeVar

from returns.primitives.exceptions import UnwrapFailedError

_ValueType_co = TypeVar('_ValueType_co', covariant=True)
_ErrorType_co = TypeVar('_ErrorType_co', covariant=True)


def partition(containers):
    """
    Partition a list of unwrappables into successful and failed values.

    Preserves order.

    .. code:: python

        >>> from returns.result import Failure, Success
        >>> from returns.methods import partition

        >>> results = [Success(1), Failure(2), Success(3), Failure(4)]
        >>> partition(results)
        ([1, 3], [2, 4])

    """
    successes = []
    failures = []
    for container in containers:
        try:
            successes.append(container.unwrap())
        except UnwrapFailedError:
            failures.append(container.failure())
    return (successes, failures)
