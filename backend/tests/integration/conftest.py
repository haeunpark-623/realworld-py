from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from realworld.db import get_db
from realworld.main import app
from realworld.models import Base


@pytest.fixture
async def integration_client() -> AsyncGenerator[AsyncClient, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    async def _override_get_db() -> AsyncGenerator:
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.pop(get_db, None)
    await engine.dispose()


async def register_user(
    client: AsyncClient, *, username: str, email: str, password: str = "supersecret"
) -> str:
    response = await client.post(
        "/api/users",
        json={"user": {"username": username, "email": email, "password": password}},
    )
    assert response.status_code == 201, response.text
    return response.json()["user"]["token"]
