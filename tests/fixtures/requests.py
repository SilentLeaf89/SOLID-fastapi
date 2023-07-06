from typing import Any
import aiohttp
import pytest_asyncio
from tests.config.settings import test_settings

@pytest_asyncio.fixture
async def make_get_request():
    # Make get request
    async def inner(path: str, query_data: dict[str, Any] = {}):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(trust_env=True)
        async with session.get(url, params=query_data) as response:
            status = response.status
            body = await response.json()
        return body, status

    return inner