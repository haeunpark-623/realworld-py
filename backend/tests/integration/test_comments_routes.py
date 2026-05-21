import pytest
from httpx import AsyncClient

from tests.integration.conftest import register_user


async def _create_article(client: AsyncClient, token: str, *, title: str = "My Post") -> dict:
    response = await client.post(
        "/api/articles",
        json={"article": {"title": title, "description": "desc", "body": "hello", "tagList": []}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 201, response.text
    return response.json()["article"]


async def _create_comment(
    client: AsyncClient, token: str, slug: str, *, body: str = "good post"
) -> dict:
    response = await client.post(
        f"/api/articles/{slug}/comments",
        json={"comment": {"body": body}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 201, response.text
    return response.json()["comment"]


@pytest.mark.asyncio
async def test_create_returns_201_with_comment(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    response = await integration_client.post(
        f"/api/articles/{article['slug']}/comments",
        json={"comment": {"body": "good post"}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 201
    body = response.json()["comment"]
    assert body["body"] == "good post"
    assert body["author"]["username"] == "jane"
    assert "createdAt" in body and "updatedAt" in body


@pytest.mark.asyncio
async def test_create_without_auth_returns_401(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    response = await integration_client.post(
        f"/api/articles/{article['slug']}/comments",
        json={"comment": {"body": "good post"}},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_for_missing_article_returns_404(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    response = await integration_client.post(
        "/api/articles/nonexistent/comments",
        json={"comment": {"body": "good post"}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_empty_body_returns_422(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    response = await integration_client.post(
        f"/api/articles/{article['slug']}/comments",
        json={"comment": {"body": ""}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_returns_comments(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    await _create_comment(integration_client, token, article["slug"], body="first")
    await _create_comment(integration_client, token, article["slug"], body="second")
    response = await integration_client.get(f"/api/articles/{article['slug']}/comments")
    assert response.status_code == 200
    body = response.json()
    assert len(body["comments"]) == 2
    assert {c["body"] for c in body["comments"]} == {"first", "second"}


@pytest.mark.asyncio
async def test_list_empty_returns_empty_array(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    response = await integration_client.get(f"/api/articles/{article['slug']}/comments")
    assert response.status_code == 200
    assert response.json() == {"comments": []}


@pytest.mark.asyncio
async def test_list_for_missing_article_returns_404(integration_client: AsyncClient) -> None:
    response = await integration_client.get("/api/articles/nonexistent/comments")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_by_author_succeeds(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    comment = await _create_comment(integration_client, token, article["slug"], body="original")
    response = await integration_client.put(
        f"/api/articles/{article['slug']}/comments/{comment['id']}",
        json={"comment": {"body": "edited"}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 200
    assert response.json()["comment"]["body"] == "edited"


@pytest.mark.asyncio
async def test_update_by_other_returns_403(integration_client: AsyncClient) -> None:
    jane_token = await register_user(integration_client, username="jane", email="jane@example.com")
    bob_token = await register_user(integration_client, username="bob", email="bob@example.com")
    article = await _create_article(integration_client, jane_token)
    comment = await _create_comment(integration_client, jane_token, article["slug"])
    response = await integration_client.put(
        f"/api/articles/{article['slug']}/comments/{comment['id']}",
        json={"comment": {"body": "hacked"}},
        headers={"Authorization": f"Token {bob_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_by_author_returns_204(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    comment = await _create_comment(integration_client, token, article["slug"])
    response = await integration_client.delete(
        f"/api/articles/{article['slug']}/comments/{comment['id']}",
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 204
    follow_up = await integration_client.get(f"/api/articles/{article['slug']}/comments")
    assert follow_up.json() == {"comments": []}


@pytest.mark.asyncio
async def test_delete_by_other_returns_403(integration_client: AsyncClient) -> None:
    jane_token = await register_user(integration_client, username="jane", email="jane@example.com")
    bob_token = await register_user(integration_client, username="bob", email="bob@example.com")
    article = await _create_article(integration_client, jane_token)
    comment = await _create_comment(integration_client, jane_token, article["slug"])
    response = await integration_client.delete(
        f"/api/articles/{article['slug']}/comments/{comment['id']}",
        headers={"Authorization": f"Token {bob_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_missing_returns_404(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token)
    response = await integration_client.delete(
        f"/api/articles/{article['slug']}/comments/9999",
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 404
