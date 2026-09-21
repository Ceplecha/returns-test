import dataclasses
import inspect
from collections.abc import Callable
from contextlib import ExitStack, contextmanager
from typing import Any, TypeVar, final, overload

import pytest
from hypothesis import given
from hypothesis import settings as hypothesis_settings
from hypothesis import strategies as st
from hypothesis.strategies._internal import types

from returns.contrib.hypothesis.containers import strategy_from_container
from returns.contrib.hypothesis.type_resolver import (
    StrategyFactory,
    strategies_for_types,
)

Example_co = TypeVar('Example_co', covariant=True)


@final
@dataclasses.dataclass(frozen=True)
class Settings:
    """
    Settings for the law tests.

    This sets the context for each generated law test, by temporarily
    registering strategies for various types and passing any ``hypothesis``
    settings.

    Any settings passed by the user will override the value from
    :func:`default_settings`.
    """

    settings_kwargs: dict[str, Any]
    use_init: bool
    container_strategy: StrategyFactory | None
    type_strategies: dict[type[object], StrategyFactory]

    def __post_init__(self):
        """Check that the settings are mutually compatible."""
        if self.use_init and self.container_strategy is not None:
            raise AssertionError(
                'Expected only one of `use_init` and `container_strategy` to be truthy'
            )

    def __or__(self, other):
        """Merge the two settings, preferring values from `other`."""
        return Settings(
            settings_kwargs=self.settings_kwargs | other.settings_kwargs,
            use_init=self.use_init | other.use_init,
            container_strategy=self.container_strategy
            if other.container_strategy is None
            else other.container_strategy,
            type_strategies=self.type_strategies | other.type_strategies,
        )


def default_settings(container_type):
    """Return default settings for creating law tests.

    We use some special strategies by default, but
    they can be overridden by the user if needed:

    - ``TypeVar``: We need to make sure that the values generated behave
      sensibly when tested for equality.

    - ``collections.abc.Callable``: We need to generate pure functions,
      which are not the default.

    Note that this is `collections.abc.Callable`, NOT `typing.Callable`. This
    is because, at runtime, `typing.get_origin(Callable[[int], str])` is
    `collections.abc.Callable`. So, this is the type we should register with
    `hypothesis`.
    """
    return Settings(
        settings_kwargs={},
        use_init=False,
        container_strategy=None,
        type_strategies={
            TypeVar: type_vars_factory,
            Callable: pure_functions_factory,
        },
    )


@overload
def check_all_laws(
    container_type,
    *,
    container_strategy,
    settings_kwargs=None,
    type_strategies=None,
): ...


@overload
def check_all_laws(container_type, *, settings_kwargs=None, use_init=False): ...


def check_all_laws(
    container_type,
    *,
    settings_kwargs=None,
    use_init=False,
    container_strategy=None,
    type_strategies=None,
):
    """
    Function to check all defined mathematical laws in a specified container.

    Should be used like so:

    .. code:: python

      from returns.contrib.hypothesis.laws import check_all_laws
      from returns.io import IO

      check_all_laws(IO)

    You can also pass different ``hypothesis`` settings inside:

    .. code:: python

      check_all_laws(IO, settings_kwargs={'max_examples': 100})

    Note:
        Cannot be used inside doctests because of the magic we use inside.

    See also:
        - https://sobolevn.me/2021/02/make-tests-a-part-of-your-app
        - https://mmhaskell.com/blog/2017/3/13/obey-the-type-laws

    """
    settings = default_settings(container_type) | Settings(
        settings_kwargs or {},
        use_init,
        container_strategy,
        type_strategies=type_strategies or {},
    )
    for interface, laws in container_type.laws().items():
        for law in laws:
            _create_law_test_case(
                container_type, interface, law, settings=settings
            )


def pure_functions_factory(thing):
    """Factory to create pure functions."""
    like = (
        (lambda: None)
        if len(thing.__args__) == 1
        else lambda *args, **kwargs: None
    )
    return_type = thing.__args__[-1]
    return st.functions(
        like=like,
        returns=st.from_type(
            type(None) if return_type is None else return_type
        ),
        pure=True,
    )


def type_vars_factory(thing):
    """
    Strategy factory for ``TypeVar`` objects.

    We ensure that values inside strategies are self-equal.
    For example, ``float('nan')`` does not work for us.
    """
    return types.resolve_TypeVar(thing).filter(lambda inner: inner == inner)


@contextmanager
def clean_plugin_context():
    """
    We register a lot of types in `_entrypoint.py`, we need to clean them.

    Otherwise, some types might be messed up.
    """
    saved_strategies = {}
    for strategy_key, strategy in types._global_type_lookup.items():
        if isinstance(
            strategy_key, type
        ) and strategy_key.__module__.startswith('returns.'):
            saved_strategies.update({strategy_key: strategy})
    for key_to_remove in saved_strategies:
        types._global_type_lookup.pop(key_to_remove)
    _clean_caches()
    try:
        yield
    finally:
        for saved_state in saved_strategies.items():
            st.register_type_strategy(*saved_state)


def _clean_caches():
    st.from_type.__clear_cache()


def _create_law_test_case(container_type, interface, law, *, settings):
    test_function = given(st.data())(
        hypothesis_settings(**settings.settings_kwargs)(
            _run_law(container_type, law, settings=settings)
        )
    )
    called_from = inspect.stack()[2]
    module = inspect.getmodule(called_from[0])
    template = 'test_{container}_{interface}_{name}'
    test_function.__name__ = template.format(
        container=container_type.__qualname__.lower(),
        interface=interface.__qualname__.lower(),
        name=law.name,
    )
    setattr(
        module,
        test_function.__name__,
        pytest.mark.filterwarnings(
            'ignore::pytest.PytestUnraisableExceptionWarning'
        )(pytest.mark.returns_lawful(test_function)),
    )


def _run_law(container_type, law, *, settings):

    def factory(source):
        with ExitStack() as stack:
            stack.enter_context(clean_plugin_context())
            stack.enter_context(
                strategies_for_types(
                    _types_to_strategies(container_type, settings)
                )
            )
            source.draw(st.builds(law.definition))

    return factory


def _types_to_strategies(container_type, settings):
    """Return a mapping from type to `hypothesis` strategy."""
    return settings.type_strategies | _container_mapping(
        container_type, settings
    )


def _container_mapping(container_type, settings):
    """Map `container_type` and its interfaces to the container strategy."""
    container_strategy = _strategy_for_container(container_type, settings)
    return {
        **dict.fromkeys(container_type.laws(), container_strategy),
        container_type: container_strategy,
    }


def _strategy_for_container(container_type, settings):
    return (
        strategy_from_container(container_type, use_init=settings.use_init)
        if settings.container_strategy is None
        else settings.container_strategy
    )
