from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from realworld.errors import Forbidden, NotFound
from realworld.models.comment import Comment
from realworld.repositories.comment import CommentRepo
from realworld.services.article import ArticleService


class CommentService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._comments = CommentRepo(session)
        self._articles = ArticleService(session)

    async def create(self, *, slug: str, author_id: int, body: str) -> Comment:
        article = await self._articles.get_by_slug(slug)
        return await self._comments.add(body=body, author_id=author_id, article_id=article.id)

    async def list_by_article(self, slug: str) -> list[Comment]:
        article = await self._articles.get_by_slug(slug)
        return await self._comments.list_by_article(article.id)

    async def update(self, *, slug: str, comment_id: int, author_id: int, body: str) -> Comment:
        article = await self._articles.get_by_slug(slug)
        comment = await self._get_comment(comment_id, article.id)
        if comment.author_id != author_id:
            raise Forbidden()
        comment.body = body
        await self._session.flush()
        await self._session.refresh(comment, attribute_names=["author"])
        return comment

    async def delete(self, *, slug: str, comment_id: int, author_id: int) -> None:
        article = await self._articles.get_by_slug(slug)
        comment = await self._get_comment(comment_id, article.id)
        if comment.author_id != author_id:
            raise Forbidden()
        await self._comments.delete(comment)

    async def _get_comment(self, comment_id: int, article_id: int) -> Comment:
        comment = await self._comments.get_by_id(comment_id)
        if comment is None or comment.article_id != article_id:
            raise NotFound("댓글을 찾을 수 없습니다")
        return comment
