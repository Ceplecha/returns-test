from returns.io import IOFailure, IOSuccess
from returns.pipeline import is_successful


def _function(arg):
    if arg == 0:
        return IOFailure(ZeroDivisionError('Divided by 0'))
    return IOSuccess(10 / arg)


def test_ioresulte():
    """Ensures that IOResultE correctly typecast."""
    container = _function(1)
    assert container == IOSuccess(10.0)
    container = _function(0)
    assert is_successful(container) is False
