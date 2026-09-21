from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from returns.primitives.hkt import dekind
from returns.result import Success

if TYPE_CHECKING:
    pass
_ValueType_co = TypeVar('_ValueType_co', covariant=True)
_NewValueType = TypeVar('_NewValueType')
_ErrorType_co = TypeVar('_ErrorType_co', covariant=True)
_EnvType = TypeVar('_EnvType')


async def async_bind_async(function, container, deps):
    """Async binds a coroutine with container over a value."""
    inner_value = await container(deps)._inner_value
    if isinstance(inner_value, Success):
        return await dekind(await function(inner_value.unwrap()))(
            deps
        )._inner_value
    return inner_value


async def async_compose_result(function, container, deps):
    """Async composes ``Result`` based function."""
    new_container = dekind(function((await container(deps))._inner_value))
    return (await new_container(deps))._inner_value
