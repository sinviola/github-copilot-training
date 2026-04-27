import asyncio

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.main import app as fastapi_app


@pytest.fixture
def app():
    return fastapi_app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def async_client(app):
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://testserver")
    yield client
    asyncio.run(client.aclose())


@pytest.fixture
def db_session():
    """Placeholder fixture for database session in this demo app."""
    return None


@pytest.fixture
def auth_token():
    """Placeholder auth token fixture for future authentication tests."""
    return "test-token"
