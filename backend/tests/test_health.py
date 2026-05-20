import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_openapi_schema_available(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    body = response.json()
    assert body["info"]["title"] == "RealWorld API"
    assert "/health" in body["paths"]


@pytest.mark.asyncio
async def test_docs_swagger_ui_available(client: AsyncClient) -> None:
    response = await client.get("/docs")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
