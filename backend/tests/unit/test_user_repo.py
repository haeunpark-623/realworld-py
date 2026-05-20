import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.repositories.user import UserRepo


@pytest.mark.asyncio
async def test_create_user_persists(db_session: AsyncSession) -> None:
    repo = UserRepo(db_session)
    user = await repo.create(
        username="alice",
        email="alice@example.com",
        password_hash="$2b$12$dummyhash",
    )
    assert user.id is not None
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.password_hash == "$2b$12$dummyhash"
    assert user.created_at is not None


@pytest.mark.asyncio
async def test_find_by_email_returns_existing(db_session: AsyncSession) -> None:
    repo = UserRepo(db_session)
    await repo.create(
        username="bob",
        email="bob@example.com",
        password_hash="$2b$12$dummyhash",
    )

    found = await repo.find_by_email("bob@example.com")
    assert found is not None
    assert found.username == "bob"


@pytest.mark.asyncio
async def test_find_by_username_returns_none_for_unknown(db_session: AsyncSession) -> None:
    repo = UserRepo(db_session)
    result = await repo.find_by_username("absent_user")
    assert result is None
