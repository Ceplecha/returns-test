from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from returns.primitives.hkt import dekind
from returns.result import Failure, Result, Success

if TYPE_CHECKING:
    pass
_ValueType_co = TypeVar('_ValueType_co', covariant=True)
_NewValueType = TypeVar('_NewValueType')
_ErrorType_co = TypeVar('_ErrorType_co', covariant=True)
_NewErrorType = TypeVar('_NewErrorType')


async def async_swap(inner_value):
    """Swaps value and error types in ``Result``."""
    return (await inner_value).swap()


async def async_map(function, inner_value):
    """Async maps a function over a value."""
    return (await inner_value).map(function)


async def async_apply(container, inner_value):
    """Async maps a function over a value."""
    return (await inner_value).apply((await container)._inner_value)


async def async_bind(function, inner_value):
    """Async binds a container over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return (await dekind(function(container.unwrap())))._inner_value
    return container


async def async_bind_awaitable(function, inner_value):
    """Async binds a coroutine over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return Result.from_value(await function(container.unwrap()))
    return container


async def async_bind_async(function, inner_value):
    """Async binds a coroutine with container over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return await dekind(await function(container.unwrap()))._inner_value
    return container


async def async_bind_result(function, inner_value):
    """Async binds a container returning ``Result`` over a value."""
    return (await inner_value).bind(function)


async def async_bind_ioresult(function, inner_value):
    """Async binds a container returning ``IOResult`` over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return function(container.unwrap())._inner_value
    return container


async def async_bind_io(function, inner_value):
    """Async binds a container returning ``IO`` over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return Success(function(container.unwrap())._inner_value)
    return container


async def async_bind_future(function, inner_value):
    """Async binds a container returning ``IO`` over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return await async_from_success(function(container.unwrap()))
    return container


async def async_bind_async_future(function, inner_value):
    """Async binds a container returning ``IO`` over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return await async_from_success(await function(container.unwrap()))
    return container


async def async_alt(function, inner_value):
    """Async alts a function over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return container
    return Failure(function(container.failure()))


async def async_lash(function, inner_value):
    """Async lashes a function returning a container over a value."""
    container = await inner_value
    if isinstance(container, Success):
        return container
    return (await dekind(function(container.failure())))._inner_value


async def async_from_success(container):
    """Async success unit factory."""
    return Success((await container)._inner_value)


async def async_from_failure(container):
    """Async failure unit factory."""
    return Failure((await container)._inner_value)


async def async_compose_result(function, inner_value):
    """Async composes ``Result`` based function."""
    return (await dekind(function(await inner_value)))._inner_value
