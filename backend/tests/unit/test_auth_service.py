import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.config import get_settings
from realworld.errors import (
    DuplicateEmail,
    DuplicateUsername,
    ExpiredToken,
    InvalidCredentials,
    InvalidToken,
)
from realworld.services.auth import AuthService
from realworld.utils.jwt import encode_token


async def test_register_creates_user_with_bcrypt_hash(db_session: AsyncSession) -> None:
    service = AuthService(db_session)
    user = await service.register(
        username="alice",
        email="alice@example.com",
        password="plaintext_pw",
    )
    assert user.id is not None
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.password_hash.startswith("$2b$12$")


async def test_register_duplicate_email_raises(db_session: AsyncSession) -> None:
    service = AuthService(db_session)
    await service.register(username="alice", email="dup@example.com", password="pw")
    with pytest.raises(DuplicateEmail):
        await service.register(username="bob", email="dup@example.com", password="pw")


async def test_register_duplicate_username_raises(db_session: AsyncSession) -> None:
    service = AuthService(db_session)
    await service.register(username="alice", email="a@example.com", password="pw")
    with pytest.raises(DuplicateUsername):
        await service.register(username="alice", email="b@example.com", password="pw")


async def test_authenticate_returns_jwt_for_valid_credentials(
    db_session: AsyncSession,
) -> None:
    service = AuthService(db_session)
    user = await service.register(username="alice", email="a@example.com", password="secret")
    token = await service.authenticate(email="a@example.com", password="secret")
    assert isinstance(token, str) and len(token) > 0
    assert (await service.get_current_user(token)).id == user.id


async def test_authenticate_wrong_password_raises_invalid_credentials(
    db_session: AsyncSession,
) -> None:
    service = AuthService(db_session)
    await service.register(username="alice", email="a@example.com", password="secret")
    with pytest.raises(InvalidCredentials):
        await service.authenticate(email="a@example.com", password="wrong")


async def test_get_current_user_returns_user_for_valid_token(
    db_session: AsyncSession,
) -> None:
    service = AuthService(db_session)
    user = await service.register(username="alice", email="a@example.com", password="secret")
    token = encode_token(user.id)
    current = await service.get_current_user(token)
    assert current.id == user.id
    assert current.email == "a@example.com"


async def test_get_current_user_expired_token_raises_expired_token(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AuthService(db_session)
    user = await service.register(username="alice", email="a@example.com", password="secret")
    get_settings.cache_clear()
    settings = get_settings()
    monkeypatch.setattr(settings, "JWT_EXPIRE_MINUTES", -1)
    token = encode_token(user.id)
    with pytest.raises(ExpiredToken):
        await service.get_current_user(token)
    get_settings.cache_clear()


async def test_get_current_user_missing_user_raises_invalid_token(
    db_session: AsyncSession,
) -> None:
    service = AuthService(db_session)
    token = encode_token(user_id=9999)
    with pytest.raises(InvalidToken):
        await service.get_current_user(token)
