from returns.context import (
    ReaderResult,
    ReaderResultE,
    RequiresContextResult,
)


def _function(arg):
    if arg == 0:
        return RequiresContextResult.from_failure(
            ZeroDivisionError('Divided by 0')
        )
    return RequiresContextResult.from_value(10 / arg)


def test_requires_context_resulte():
    """Ensures that RequiresContextResultE correctly typecast."""
    container = _function(1)
    assert container(0) == RequiresContextResult.from_value(10.0)(0)


def test_requires_context_aliases():
    """Ensures that ReaderResult correctly typecast."""
    container = _function(1)
    container2 = _function(1)
    container3 = ReaderResultE.from_value(10.0)
    container4 = ReaderResult.from_value(10.0)
    assert container(0) == container2(0) == container3(0) == container4(0)
    assert container(0) == RequiresContextResult.from_value(10.0)(0)
