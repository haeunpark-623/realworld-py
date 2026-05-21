"""Seed dev DB with 10 users + 100 articles + 5 tags (idempotent).

Usage: (cd backend && uv run python -m scripts.seed_articles)

Idempotent — DELETE all then INSERT. random.seed(42) fixed for reproducibility.
"""

from __future__ import annotations

import asyncio
import random

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.db import async_session_maker
from realworld.models import Article, Tag, User, article_tags
from realworld.utils.security import hash_password

USER_COUNT = 10
ARTICLE_COUNT = 100
TAG_NAMES = ["python", "fastapi", "react", "sqlalchemy", "realworld"]
SEED_PASSWORD = "seed-password"


async def seed(session: AsyncSession) -> dict[str, int]:
    """Wipe + reseed. Returns counts.

    Order matters for FK CASCADE — article_tags M2M → articles → tags → users.
    """
    random.seed(42)

    await session.execute(delete(article_tags))
    await session.execute(delete(Article))
    await session.execute(delete(Tag))
    await session.execute(delete(User))
    await session.flush()

    password_hash = hash_password(SEED_PASSWORD)
    users = [
        User(
            username=f"seed_user_{i}",
            email=f"seed_user_{i}@example.com",
            password_hash=password_hash,
        )
        for i in range(1, USER_COUNT + 1)
    ]
    session.add_all(users)
    await session.flush()

    tags = [Tag(name=name) for name in TAG_NAMES]
    session.add_all(tags)
    await session.flush()

    for i in range(1, ARTICLE_COUNT + 1):
        author = users[(i - 1) % USER_COUNT]
        article = Article(
            slug=f"seed-article-{i}",
            title=f"Seed Article #{i}",
            description=f"Description for seed article {i}.",
            body=f"Sample article body #{i}. Lorem ipsum dolor sit amet.",
            author_id=author.id,
        )
        tag_count = random.randint(0, 3)
        if tag_count > 0:
            article.tags = random.sample(tags, tag_count)
        session.add(article)

    await session.flush()

    counts = {
        "users": (await session.execute(select(User))).scalars().all().__len__(),
        "articles": (await session.execute(select(Article))).scalars().all().__len__(),
        "tags": (await session.execute(select(Tag))).scalars().all().__len__(),
    }
    return counts


async def main() -> None:
    async with async_session_maker() as session:
        async with session.begin():
            counts = await seed(session)
    print(f"users={counts['users']} articles={counts['articles']} tags={counts['tags']}")


if __name__ == "__main__":
    asyncio.run(main())
