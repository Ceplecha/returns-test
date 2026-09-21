import pickle

from returns.maybe import Nothing
from returns.primitives.exceptions import UnwrapFailedError
from returns.result import Failure


def test_pickle_unwrap_failed_error_from_maybe():
    """Ensures that UnwrapFailedError with Maybe can be pickled."""
    serialized = None
    try:
        Nothing.unwrap()
    except UnwrapFailedError as error:
        serialized = pickle.dumps(error)
    deserialized_error = pickle.loads(serialized)
    assert deserialized_error.halted_container == Nothing


def test_pickle_unwrap_failed_error_from_result():
    """Ensures that UnwrapFailedError with Result can be pickled."""
    serialized = None
    try:
        Failure('error').unwrap()
    except UnwrapFailedError as error:
        serialized = pickle.dumps(error)
    deserialized_error = pickle.loads(serialized)
    assert deserialized_error.halted_container == Failure('error')
