import pytest
from httpx import AsyncClient

from tests.integration.conftest import register_user


@pytest.mark.asyncio
async def test_list_tags_returns_distinct_tag_names_sorted(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    for tag_list in ([], ["python", "fastapi"], ["react", "python"]):
        response = await integration_client.post(
            "/api/articles",
            json={
                "article": {
                    "title": f"post {tag_list}",
                    "description": None,
                    "body": "b",
                    "tagList": tag_list,
                }
            },
            headers={"Authorization": f"Token {token}"},
        )
        assert response.status_code == 201, response.text

    response = await integration_client.get("/api/tags")
    assert response.status_code == 200
    body = response.json()
    assert body == {"tags": ["fastapi", "python", "react"]}


@pytest.mark.asyncio
async def test_list_tags_empty(integration_client: AsyncClient) -> None:
    response = await integration_client.get("/api/tags")
    assert response.status_code == 200
    assert response.json() == {"tags": []}
