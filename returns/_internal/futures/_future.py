from typing import TYPE_CHECKING, TypeVar

from returns.primitives.hkt import dekind

if TYPE_CHECKING:
    pass
_ValueType_co = TypeVar('_ValueType_co', covariant=True)
_NewValueType = TypeVar('_NewValueType')


async def async_map(function, inner_value):
    """Async maps a function over a value."""
    return function(await inner_value)


async def async_apply(container, inner_value):
    """Async applies a container with function over a value."""
    return (await container)._inner_value(await inner_value)


async def async_bind(function, inner_value):
    """Async binds a container over a value."""
    return (await dekind(function(await inner_value)))._inner_value


async def async_bind_awaitable(function, inner_value):
    """Async binds a coroutine over a value."""
    return await function(await inner_value)


async def async_bind_async(function, inner_value):
    """Async binds a coroutine with container over a value."""
    inner_io = dekind(await function(await inner_value))._inner_value
    return await inner_io


async def async_bind_io(function, inner_value):
    """Async binds a container over a value."""
    return function(await inner_value)._inner_value
