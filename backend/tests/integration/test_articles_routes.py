import pytest
from httpx import AsyncClient

from tests.integration.conftest import register_user


async def _create_article(
    client: AsyncClient, token: str, *, title: str = "My Post", body: str = "hello"
) -> dict:
    response = await client.post(
        "/api/articles",
        json={"article": {"title": title, "description": "desc", "body": body, "tagList": []}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 201, response.text
    return response.json()["article"]


@pytest.mark.asyncio
async def test_list_returns_articles_and_count(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    await _create_article(integration_client, token, title="Post A")
    await _create_article(integration_client, token, title="Post B")

    response = await integration_client.get("/api/articles")
    assert response.status_code == 200
    body = response.json()
    assert body["articlesCount"] == 2
    assert len(body["articles"]) == 2


@pytest.mark.asyncio
async def test_list_with_author_filter_returns_only_authors_articles(
    integration_client: AsyncClient,
) -> None:
    jane_token = await register_user(integration_client, username="jane", email="jane@example.com")
    bob_token = await register_user(integration_client, username="bob", email="bob@example.com")
    await _create_article(integration_client, jane_token, title="Jane Post 1")
    await _create_article(integration_client, jane_token, title="Jane Post 2")
    await _create_article(integration_client, bob_token, title="Bob Post")

    response = await integration_client.get("/api/articles?author=jane")
    assert response.status_code == 200
    body = response.json()
    assert body["articlesCount"] == 2
    assert all(a["author"]["username"] == "jane" for a in body["articles"])


@pytest.mark.asyncio
async def test_list_with_unknown_author_returns_empty(integration_client: AsyncClient) -> None:
    response = await integration_client.get("/api/articles?author=nobody")
    assert response.status_code == 200
    assert response.json() == {"articles": [], "articlesCount": 0}


@pytest.mark.asyncio
async def test_detail_returns_article(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token, title="My Post")
    response = await integration_client.get(f"/api/articles/{article['slug']}")
    assert response.status_code == 200
    body = response.json()["article"]
    assert body["title"] == "My Post"
    assert body["author"]["username"] == "jane"


@pytest.mark.asyncio
async def test_detail_missing_returns_404(integration_client: AsyncClient) -> None:
    response = await integration_client.get("/api/articles/nonexistent")
    assert response.status_code == 404
    assert "찾을 수 없습니다" in response.json()["errors"]["body"][0]


@pytest.mark.asyncio
async def test_create_returns_201_with_article(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    response = await integration_client.post(
        "/api/articles",
        json={
            "article": {
                "title": "My Post",
                "description": "desc",
                "body": "hello",
                "tagList": ["intro", "test"],
            }
        },
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 201
    body = response.json()["article"]
    assert body["slug"] == "my-post"
    assert set(body["tagList"]) == {"intro", "test"}
    assert body["author"]["username"] == "jane"


@pytest.mark.asyncio
async def test_create_without_auth_returns_401(integration_client: AsyncClient) -> None:
    response = await integration_client.post(
        "/api/articles",
        json={"article": {"title": "My Post", "description": None, "body": "b", "tagList": []}},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_duplicate_title_assigns_suffix_slug(
    integration_client: AsyncClient,
) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    first = await _create_article(integration_client, token, title="My Post")
    second = await _create_article(integration_client, token, title="My Post", body="b2")
    assert first["slug"] == "my-post"
    assert second["slug"] == "my-post-2"


@pytest.mark.asyncio
async def test_update_by_author_succeeds(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token, title="Original")
    response = await integration_client.put(
        f"/api/articles/{article['slug']}",
        json={"article": {"title": "Renamed"}},
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 200
    assert response.json()["article"]["title"] == "Renamed"


@pytest.mark.asyncio
async def test_update_by_other_returns_403(integration_client: AsyncClient) -> None:
    jane_token = await register_user(integration_client, username="jane", email="jane@example.com")
    bob_token = await register_user(integration_client, username="bob", email="bob@example.com")
    article = await _create_article(integration_client, jane_token, title="Janes Post")
    response = await integration_client.put(
        f"/api/articles/{article['slug']}",
        json={"article": {"title": "Hacked"}},
        headers={"Authorization": f"Token {bob_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_by_author_returns_204(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token, title="Trash")
    response = await integration_client.delete(
        f"/api/articles/{article['slug']}",
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == 204
    follow_up = await integration_client.get(f"/api/articles/{article['slug']}")
    assert follow_up.status_code == 404


@pytest.mark.asyncio
async def test_delete_by_other_returns_403(integration_client: AsyncClient) -> None:
    jane_token = await register_user(integration_client, username="jane", email="jane@example.com")
    bob_token = await register_user(integration_client, username="bob", email="bob@example.com")
    article = await _create_article(integration_client, jane_token, title="Janes Post")
    response = await integration_client.delete(
        f"/api/articles/{article['slug']}",
        headers={"Authorization": f"Token {bob_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_cascades_comments(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    article = await _create_article(integration_client, token, title="Soon Deleted")
    for body in ("first", "second"):
        response = await integration_client.post(
            f"/api/articles/{article['slug']}/comments",
            json={"comment": {"body": body}},
            headers={"Authorization": f"Token {token}"},
        )
        assert response.status_code == 201, response.text

    list_before = await integration_client.get(f"/api/articles/{article['slug']}/comments")
    assert len(list_before.json()["comments"]) == 2

    delete_resp = await integration_client.delete(
        f"/api/articles/{article['slug']}",
        headers={"Authorization": f"Token {token}"},
    )
    assert delete_resp.status_code == 204

    list_after = await integration_client.get(f"/api/articles/{article['slug']}/comments")
    assert list_after.status_code == 404
    assert "찾을 수 없습니다" in list_after.json()["errors"]["body"][0]
