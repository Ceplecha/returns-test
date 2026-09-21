import pytest

from returns.future import Future, FutureResult
from returns.io import IO


@pytest.mark.anyio
async def test_inner_value(subtests):
    """Ensure that coroutine correct value is preserved for all units."""
    containers = [
        Future.from_value(1),
        Future.from_io(IO(1)),
        Future.from_future_result(FutureResult.from_value(1)),
        Future.from_future_result(FutureResult.from_failure(1)),
    ]
    for container in containers:
        with subtests.test(container=container):
            assert isinstance(await container, IO)
