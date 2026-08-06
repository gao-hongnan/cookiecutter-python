{% if cookiecutter.use_fastapi %}"""Tests for the {{ cookiecutter.project_name }} FastAPI application."""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from {{ cookiecutter.package_name }}.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Drive the app in-process, without binding a port.

    Yields
    ------
    AsyncClient
        Client wired straight to the ASGI app.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


async def test_root_returns_greeting(client: AsyncClient) -> None:
    """The root endpoint returns the greeting payload."""
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello from {{ cookiecutter.project_name }}"}


async def test_health_reports_healthy(client: AsyncClient) -> None:
    """The health endpoint reports a healthy status."""
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


async def test_unknown_route_returns_404(client: AsyncClient) -> None:
    """Unregistered paths return 404 rather than erroring."""
    response = await client.get("/does-not-exist")

    assert response.status_code == 404
{%- endif %}
