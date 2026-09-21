from collections.abc import Callable
from typing import TypeVar

import pytest
from hypothesis import given
from hypothesis import strategies as st

from returns.context import (
    Reader,
    RequiresContext,
    RequiresContextFutureResult,
    RequiresContextFutureResultE,
    RequiresContextIOResult,
    RequiresContextIOResultE,
    RequiresContextResult,
    RequiresContextResultE,
)
from returns.contrib.hypothesis.laws import (
    Settings,
    _types_to_strategies,
    default_settings,
)
from returns.contrib.hypothesis.type_resolver import (
    apply_strategy,
    look_up_strategy,
)
from returns.future import Future, FutureResult
from returns.interfaces.applicative import ApplicativeN
from returns.io import IO, IOResult, IOResultE
from returns.maybe import Maybe
from returns.pipeline import is_successful
from returns.result import Result, ResultE
from test_hypothesis.test_laws import test_custom_type_applicative

_all_containers = (
    Maybe,
    Result,
    IO,
    IOResult,
    Future,
    FutureResult,
    RequiresContext,
    RequiresContextResult,
    RequiresContextIOResult,
    RequiresContextFutureResult,
    ResultE,
    IOResultE,
    Reader,
    RequiresContextResultE,
    RequiresContextIOResultE,
    RequiresContextFutureResultE,
)


@pytest.mark.filterwarnings('ignore:.*')
@pytest.mark.parametrize('container_type', _all_containers)
def test_all_containers_resolves(container_type):
    """Ensures all containers do resolve."""
    assert st.from_type(container_type).example() is not None


@given(
    st.from_type(ResultE).filter(lambda container: not is_successful(container))
)
def test_result_error_alias_resolves(thing):
    """Ensures that type aliases are resolved correctly."""
    assert isinstance(thing.failure(), Exception)


CustomResult = Result[int, str]


@given(st.from_type(CustomResult))
def test_custom_result_error_types_resolve(thing):
    """Ensures that type aliases are resolved correctly."""
    if is_successful(thing):
        assert isinstance(thing.unwrap(), int)
    else:
        assert isinstance(thing.failure(), str)


@given(
    st.from_type(RequiresContextResultE).filter(
        lambda container: (
            not is_successful(container(RequiresContextResultE.no_args))
        )
    )
)
def test_reader_result_error_alias_resolves(thing):
    """Ensures that type aliases are resolved correctly."""
    real_result = thing(RequiresContextResultE.no_args)
    assert isinstance(real_result.failure(), Exception)


CustomReaderResult = RequiresContextResult[int, str, bool]


@given(st.from_type(CustomReaderResult))
def test_custom_readerresult_types_resolve(thing):
    """Ensures that type aliases are resolved correctly."""
    real_result = thing(RequiresContextResultE.no_args)
    if is_successful(real_result):
        assert isinstance(real_result.unwrap(), int)
    else:
        assert isinstance(real_result.failure(), str)


def test_merge_settings():
    """Check that each part of the settings can be overridden by users."""
    settings1 = Settings(
        settings_kwargs={'a': 1, 'b': 2},
        use_init=False,
        container_strategy=st.integers(),
        type_strategies={int: st.integers(max_value=10), str: st.text('abc')},
    )
    settings2 = Settings(
        settings_kwargs={'a': 1, 'c': 3},
        use_init=False,
        container_strategy=st.integers(max_value=20),
        type_strategies={int: st.integers(max_value=30), bool: st.booleans()},
    )
    result = settings1 | settings2
    assert result == Settings(
        settings_kwargs={'a': 1, 'b': 2, 'c': 3},
        use_init=False,
        container_strategy=st.integers(max_value=20),
        type_strategies={
            int: st.integers(max_value=30),
            bool: st.booleans(),
            str: st.text('abc'),
        },
    )


def test_merge_use_init():
    """Check that `use_init` can be set to `True` by users.

    Note: They can't set a `True` to `False`, since we use `|` to merge.
    However, the default value is `False`, so this should not be a problem.
    """
    settings1 = Settings(
        settings_kwargs={},
        use_init=False,
        container_strategy=None,
        type_strategies={},
    )
    settings2 = Settings(
        settings_kwargs={},
        use_init=True,
        container_strategy=None,
        type_strategies={},
    )
    result = settings1 | settings2
    assert result == Settings(
        settings_kwargs={},
        use_init=True,
        container_strategy=None,
        type_strategies={},
    )


_ValueType = TypeVar('_ValueType')


def test_types_to_strategies_default():
    """Check the default strategies for types."""
    container_type = test_custom_type_applicative._Wrapper
    callable_type = Callable
    result = _types_to_strategies(
        container_type, default_settings(container_type)
    )
    wrapper_strategy = _strategy_string(result[container_type], container_type)
    assert 'builds' in wrapper_strategy
    assert 'from_value' in wrapper_strategy
    assert 'sampled_from' in wrapper_strategy
    assert 'from_type' in wrapper_strategy
    interface_reprs = _strategy_strings(
        [result[interface] for interface in container_type.laws()],
        container_type,
    )
    assert all(
        ('builds' in interface_repr for interface_repr in interface_reprs)
    )
    assert all(
        ('from_value' in interface_repr for interface_repr in interface_reprs)
    )
    functions_with_args = _strategy_string(
        result[callable_type], Callable[[int, str], bool]
    )
    assert 'functions' in functions_with_args
    assert 'booleans' in functions_with_args
    functions_no_args = _strategy_string(
        result[callable_type], Callable[[], None]
    )
    assert 'functions' in functions_no_args
    assert 'none' in functions_no_args
    typevar_strategy = _strategy_string(result[TypeVar], _ValueType)
    assert 'sampled_from' in typevar_strategy
    assert 'from_type' in typevar_strategy


def test_types_to_strategies_overrides():
    """Check that we allow the user to override all strategies."""
    container_type = test_custom_type_applicative._Wrapper
    callable_type = Callable
    result = _types_to_strategies(
        container_type,
        Settings(
            settings_kwargs={},
            use_init=False,
            container_strategy=st.builds(container_type, st.integers()),
            type_strategies={
                TypeVar: st.text(),
                callable_type: st.functions(returns=st.booleans()),
                ApplicativeN: st.tuples(st.integers()),
            },
        ),
    )
    wrapper_strategy = _strategy_string(result[container_type], container_type)
    assert 'builds' in wrapper_strategy
    assert '_Wrapper' in wrapper_strategy
    assert 'integers' in wrapper_strategy
    interface_reprs = _strategy_strings(
        [result[interface] for interface in container_type.laws()],
        container_type,
    )
    assert all(
        ('builds' in interface_repr for interface_repr in interface_reprs)
    )
    assert all(
        ('_Wrapper' in interface_repr for interface_repr in interface_reprs)
    )
    assert all(
        ('integers' in interface_repr for interface_repr in interface_reprs)
    )
    functions_with_args = _strategy_string(
        result[callable_type], Callable[[int, str], bool]
    )
    assert 'functions' in functions_with_args
    assert 'booleans' in functions_with_args
    functions_no_args = _strategy_string(
        result[callable_type], Callable[[], None]
    )
    assert 'functions' in functions_no_args
    assert 'booleans' in functions_no_args
    assert 'text' in _strategy_string(result[TypeVar], _ValueType)


def _interface_factories(type_):
    return [look_up_strategy(interface) for interface in type_.laws()]


def _strategy_strings(strategy_factories, type_):
    return [
        _strategy_string(strategy_factory, type_)
        for strategy_factory in strategy_factories
    ]


def _strategy_string(strategy_factory, type_):
    """Return an easily testable string representation."""
    return (
        str(None)
        if strategy_factory is None
        else str(apply_strategy(strategy_factory, type_))
    )
