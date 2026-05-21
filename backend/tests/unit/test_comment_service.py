import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.errors import Forbidden, NotFound
from realworld.repositories.user import UserRepo
from realworld.services.article import ArticleService
from realworld.services.comment import CommentService


async def _create_user(session: AsyncSession, *, username: str, email: str) -> int:
    user = await UserRepo(session).create(
        username=username, email=email, password_hash="$2b$12$dummyhash"
    )
    return user.id


async def _create_article(session: AsyncSession, *, author_id: int, title: str = "My Post") -> str:
    article = await ArticleService(session).create(
        author_id=author_id, title=title, description=None, body="b", tag_list=[]
    )
    return article.slug


@pytest.mark.asyncio
async def test_create_returns_comment_with_author(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    slug = await _create_article(db_session, author_id=author_id)
    service = CommentService(db_session)
    comment = await service.create(slug=slug, author_id=author_id, body="good post")
    assert comment.body == "good post"
    assert comment.author.username == "jane"


@pytest.mark.asyncio
async def test_create_for_missing_article_raises_not_found(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    service = CommentService(db_session)
    with pytest.raises(NotFound):
        await service.create(slug="nonexistent", author_id=author_id, body="hi")


@pytest.mark.asyncio
async def test_list_returns_comments_in_recent_order(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    slug = await _create_article(db_session, author_id=author_id)
    service = CommentService(db_session)
    await service.create(slug=slug, author_id=author_id, body="first")
    await service.create(slug=slug, author_id=author_id, body="second")
    comments = await service.list_by_article(slug)
    assert len(comments) == 2
    bodies = {c.body for c in comments}
    assert bodies == {"first", "second"}


@pytest.mark.asyncio
async def test_list_for_missing_article_raises_not_found(db_session: AsyncSession) -> None:
    service = CommentService(db_session)
    with pytest.raises(NotFound):
        await service.list_by_article("nonexistent")


@pytest.mark.asyncio
async def test_list_for_article_without_comments_returns_empty(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    slug = await _create_article(db_session, author_id=author_id)
    service = CommentService(db_session)
    comments = await service.list_by_article(slug)
    assert comments == []


@pytest.mark.asyncio
async def test_update_by_author_changes_body(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    slug = await _create_article(db_session, author_id=author_id)
    service = CommentService(db_session)
    comment = await service.create(slug=slug, author_id=author_id, body="original")
    updated = await service.update(
        slug=slug, comment_id=comment.id, author_id=author_id, body="edited"
    )
    assert updated.body == "edited"


@pytest.mark.asyncio
async def test_update_by_other_user_raises_forbidden(db_session: AsyncSession) -> None:
    jane_id = await _create_user(db_session, username="jane", email="jane@example.com")
    bob_id = await _create_user(db_session, username="bob", email="bob@example.com")
    slug = await _create_article(db_session, author_id=jane_id)
    service = CommentService(db_session)
    comment = await service.create(slug=slug, author_id=jane_id, body="janes")
    with pytest.raises(Forbidden):
        await service.update(slug=slug, comment_id=comment.id, author_id=bob_id, body="hacked")


@pytest.mark.asyncio
async def test_update_missing_comment_raises_not_found(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    slug = await _create_article(db_session, author_id=author_id)
    service = CommentService(db_session)
    with pytest.raises(NotFound):
        await service.update(slug=slug, comment_id=9999, author_id=author_id, body="x")


@pytest.mark.asyncio
async def test_delete_by_author_succeeds(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    slug = await _create_article(db_session, author_id=author_id)
    service = CommentService(db_session)
    comment = await service.create(slug=slug, author_id=author_id, body="bye")
    await service.delete(slug=slug, comment_id=comment.id, author_id=author_id)
    remaining = await service.list_by_article(slug)
    assert remaining == []


@pytest.mark.asyncio
async def test_delete_by_other_user_raises_forbidden(db_session: AsyncSession) -> None:
    jane_id = await _create_user(db_session, username="jane", email="jane@example.com")
    bob_id = await _create_user(db_session, username="bob", email="bob@example.com")
    slug = await _create_article(db_session, author_id=jane_id)
    service = CommentService(db_session)
    comment = await service.create(slug=slug, author_id=jane_id, body="janes")
    with pytest.raises(Forbidden):
        await service.delete(slug=slug, comment_id=comment.id, author_id=bob_id)


@pytest.mark.asyncio
async def test_delete_missing_comment_raises_not_found(db_session: AsyncSession) -> None:
    author_id = await _create_user(db_session, username="jane", email="jane@example.com")
    slug = await _create_article(db_session, author_id=author_id)
    service = CommentService(db_session)
    with pytest.raises(NotFound):
        await service.delete(slug=slug, comment_id=9999, author_id=author_id)
