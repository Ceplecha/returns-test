from returns.io import IOFailure, IOSuccess
from returns.result import Failure, Success


def test_bind():
    """Ensures that bind works."""

    def factory(inner_value):
        if inner_value > 0:
            return IOSuccess(inner_value * 2)
        return IOFailure(str(inner_value))

    input_value = 5
    bound = IOSuccess(input_value)
    assert bound.bind(factory) == factory(input_value)
    assert str(bound.bind(factory)) == '<IOResult: <Success: 10>>'
    input_value = 0
    bound2 = IOSuccess(input_value)
    assert bound2.bind(factory) == factory(input_value)
    assert str(bound2.bind(factory)) == '<IOResult: <Failure: 0>>'


def test_left_identity_success():
    """Ensures that left identity works for IOSuccess container."""

    def factory(inner_value):
        return IOSuccess(inner_value * 2)

    input_value = 5
    bound = IOSuccess(input_value)
    assert bound.bind(factory) == factory(input_value)


def test_left_identity_failure():
    """Ensures that left identity works for IOFailure container."""

    def factory(inner_value):
        return IOFailure(6)

    input_value = 5
    bound = IOFailure(input_value)
    assert bound.bind(factory) == IOFailure(input_value)


def test_bind_regular_result():
    """Ensures that regular ``Result`` can be bound to ``IOResult``."""

    def factory(inner_value):
        if inner_value > 0:
            return Success(inner_value + 1)
        return Failure('nope')

    first = IOSuccess(1)
    second = IOSuccess(0)
    third = IOFailure('a')
    assert first.bind_result(factory) == IOSuccess(2)
    assert second.bind_result(factory) == IOFailure('nope')
    assert third.bind_result(factory) == IOFailure('a')


def test_lash_success():
    """Ensures that lash works for IOSuccess container."""

    def factory(inner_value):
        return IOSuccess(inner_value * 2)

    assert IOSuccess(5).lash(factory) == IOSuccess(5)


def test_lash_failure():
    """Ensures that lash works for IOFailure container."""

    def factory(inner_value):
        return IOFailure(inner_value + 1)

    expected = 6
    bound = IOFailure(5)
    assert bound.lash(factory) == IOFailure(expected)
