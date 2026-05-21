import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.errors import Forbidden, NotFound
from realworld.repositories.user import UserRepo
from realworld.services.article import ArticleService


async def _create_user(session: AsyncSession, *, username: str, email: str) -> int:
    user = await UserRepo(session).create(
        username=username, email=email, password_hash="$2b$12$dummyhash"
    )
    return user.id


@pytest.mark.asyncio
async def test_create_article_assigns_slug_and_tags(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    service = ArticleService(db_session)
    article = await service.create(
        author_id=author_id,
        title="My First Article",
        description="desc",
        body="hello",
        tag_list=["intro", "test"],
    )
    assert article.slug == "my-first-article"
    assert {tag.name for tag in article.tags} == {"intro", "test"}


@pytest.mark.asyncio
async def test_create_article_progresses_suffix_on_slug_conflict(
    db_session: AsyncSession,
) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    service = ArticleService(db_session)
    first = await service.create(
        author_id=author_id, title="My Post", description=None, body="b1", tag_list=[]
    )
    second = await service.create(
        author_id=author_id, title="My Post", description=None, body="b2", tag_list=[]
    )
    third = await service.create(
        author_id=author_id, title="My Post", description=None, body="b3", tag_list=[]
    )
    assert first.slug == "my-post"
    assert second.slug == "my-post-2"
    assert third.slug == "my-post-3"


@pytest.mark.asyncio
async def test_list_returns_articles_with_count(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    service = ArticleService(db_session)
    for i in range(3):
        await service.create(
            author_id=author_id,
            title=f"Post {i}",
            description=None,
            body="b",
            tag_list=[],
        )
    articles, total = await service.list(limit=20, offset=0, author=None)
    assert total == 3
    assert len(articles) == 3


@pytest.mark.asyncio
async def test_get_by_slug_raises_not_found_for_missing(db_session: AsyncSession) -> None:
    service = ArticleService(db_session)
    with pytest.raises(NotFound):
        await service.get_by_slug("nonexistent")


@pytest.mark.asyncio
async def test_update_by_author_changes_fields(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    service = ArticleService(db_session)
    article = await service.create(
        author_id=author_id, title="Original", description=None, body="b", tag_list=[]
    )
    updated = await service.update(
        slug=article.slug,
        author_id=author_id,
        title="Renamed",
        description=None,
        body=None,
        tag_list=None,
    )
    assert updated.title == "Renamed"
    assert updated.body == "b"


@pytest.mark.asyncio
async def test_update_by_other_user_raises_forbidden(db_session: AsyncSession) -> None:
    jane_id = await _create_user(db_session, username="jane", email="jane@example.com")
    bob_id = await _create_user(db_session, username="bob", email="bob@example.com")
    service = ArticleService(db_session)
    article = await service.create(
        author_id=jane_id, title="My Post", description=None, body="b", tag_list=[]
    )
    with pytest.raises(Forbidden):
        await service.update(
            slug=article.slug,
            author_id=bob_id,
            title="Hacked",
            description=None,
            body=None,
            tag_list=None,
        )


@pytest.mark.asyncio
async def test_delete_by_author_succeeds(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    service = ArticleService(db_session)
    article = await service.create(
        author_id=author_id, title="My Post", description=None, body="b", tag_list=[]
    )
    await service.delete(slug=article.slug, author_id=author_id)
    with pytest.raises(NotFound):
        await service.get_by_slug(article.slug)


@pytest.mark.asyncio
async def test_delete_by_other_user_raises_forbidden(db_session: AsyncSession) -> None:
    jane_id = await _create_user(db_session, username="jane", email="jane@example.com")
    bob_id = await _create_user(db_session, username="bob", email="bob@example.com")
    service = ArticleService(db_session)
    article = await service.create(
        author_id=jane_id, title="My Post", description=None, body="b", tag_list=[]
    )
    with pytest.raises(Forbidden):
        await service.delete(slug=article.slug, author_id=bob_id)
