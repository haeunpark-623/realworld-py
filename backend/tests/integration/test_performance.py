"""R-N-01 — GET /api/articles?limit=20 p95 < 200ms (seed: 100 articles, 10 users, 5 tags)."""

from __future__ import annotations

import statistics
import time
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from realworld.db import get_db
from realworld.main import app
from realworld.models import Base
from scripts.seed_articles import seed

P95_THRESHOLD_SECONDS = 0.200
WARMUP_CALLS = 10
MEASURED_CALLS = 90
TOTAL_CALLS = WARMUP_CALLS + MEASURED_CALLS


@pytest.fixture
async def seeded_client() -> AsyncGenerator[AsyncClient, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    async with session_maker() as setup_session, setup_session.begin():
        await seed(setup_session)

    async def _override_get_db() -> AsyncGenerator:
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.pop(get_db, None)
    await engine.dispose()


async def test_articles_list_p95(seeded_client: AsyncClient) -> None:
    latencies: list[float] = []
    for _ in range(TOTAL_CALLS):
        start = time.perf_counter()
        response = await seeded_client.get("/api/articles", params={"limit": 20})
        elapsed = time.perf_counter() - start
        assert response.status_code == 200, response.text
        latencies.append(elapsed)

    measured = latencies[WARMUP_CALLS:]
    assert len(measured) == MEASURED_CALLS

    quantiles = statistics.quantiles(measured, n=20)
    p95 = quantiles[18]
    p50 = statistics.median(measured)
    print(
        f"\n[R-N-01 measurement] "
        f"calls={TOTAL_CALLS} (warmup={WARMUP_CALLS}, measured={MEASURED_CALLS}) "
        f"p50={p50 * 1000:.2f}ms p95={p95 * 1000:.2f}ms "
        f"threshold={P95_THRESHOLD_SECONDS * 1000:.0f}ms"
    )
    assert p95 < P95_THRESHOLD_SECONDS, (
        f"R-N-01 미달: p95={p95 * 1000:.2f}ms ≥ {P95_THRESHOLD_SECONDS * 1000:.0f}ms"
    )

    body = response.json()
    assert body["articlesCount"] == 100
    assert len(body["articles"]) == 20
