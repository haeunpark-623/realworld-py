import pytest
from httpx import AsyncClient

from tests.integration.conftest import register_user


@pytest.mark.asyncio
async def test_register_returns_user_with_token(integration_client: AsyncClient) -> None:
    response = await integration_client.post(
        "/api/users",
        json={
            "user": {
                "username": "jane",
                "email": "jane@example.com",
                "password": "supersecret",
            }
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["username"] == "jane"
    assert body["user"]["email"] == "jane@example.com"
    assert body["user"]["token"]
    assert body["user"]["bio"] is None
    assert body["user"]["image"] is None


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_422(integration_client: AsyncClient) -> None:
    await register_user(integration_client, username="jane", email="jane@example.com")
    response = await integration_client.post(
        "/api/users",
        json={
            "user": {
                "username": "jane2",
                "email": "jane@example.com",
                "password": "supersecret",
            }
        },
    )
    assert response.status_code == 422
    assert "이메일" in response.json()["errors"]["body"][0]


@pytest.mark.asyncio
async def test_register_short_password_returns_422(integration_client: AsyncClient) -> None:
    response = await integration_client.post(
        "/api/users",
        json={"user": {"username": "jane", "email": "jane@example.com", "password": "short"}},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_returns_user_with_token(integration_client: AsyncClient) -> None:
    await register_user(integration_client, username="jane", email="jane@example.com")
    response = await integration_client.post(
        "/api/users/login",
        json={"user": {"email": "jane@example.com", "password": "supersecret"}},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["user"]["username"] == "jane"
    assert body["user"]["token"]


@pytest.mark.asyncio
async def test_login_invalid_credentials_returns_422(integration_client: AsyncClient) -> None:
    await register_user(integration_client, username="jane", email="jane@example.com")
    response = await integration_client.post(
        "/api/users/login",
        json={"user": {"email": "jane@example.com", "password": "wrongpassword"}},
    )
    assert response.status_code == 422
    assert "이메일 또는 비밀번호" in response.json()["errors"]["body"][0]


@pytest.mark.asyncio
async def test_current_user_with_jwt_returns_user(integration_client: AsyncClient) -> None:
    token = await register_user(integration_client, username="jane", email="jane@example.com")
    response = await integration_client.get(
        "/api/user", headers={"Authorization": f"Token {token}"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "jane"


@pytest.mark.asyncio
async def test_current_user_without_auth_returns_401(integration_client: AsyncClient) -> None:
    response = await integration_client.get("/api/user")
    assert response.status_code == 401
    assert "인증 토큰" in response.json()["errors"]["body"][0]
