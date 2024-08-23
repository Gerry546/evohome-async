#!/usr/bin/env python3
"""evohome-async - test config."""

import logging
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio

from .faked_server import FakedServer
from .helpers import aiohttp

# normally, we want these debug flags to be False
_DBG_USE_REAL_AIOHTTP = False
_DBG_DISABLE_STRICT_ASSERTS = False  # of response content-type, schema

_LOGGER = logging.getLogger(__name__)


#######################################################################################


@pytest.fixture(autouse=True)
def patches_for_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("evohomeasync2.base.aiohttp", aiohttp)
    monkeypatch.setattr("evohomeasync2.broker.aiohttp", aiohttp)

    monkeypatch.setattr("evohomeasync.base.aiohttp", aiohttp)
    monkeypatch.setattr("evohomeasync.broker.aiohttp", aiohttp)


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    if _DBG_USE_REAL_AIOHTTP:
        client_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
    else:
        client_session = aiohttp.ClientSession(faked_server=FakedServer(None, None))  # type: ignore[call-arg]

    try:
        yield client_session
    finally:
        await client_session.close()


@pytest.fixture()
def user_credentials() -> tuple[str, str]:
    username: str = os.getenv("TEST_USERNAME") or "username@email.com"
    password: str = os.getenv("TEST_PASSWORD") or "password!"

    return username, password
