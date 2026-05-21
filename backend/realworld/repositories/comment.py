from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from realworld.models.comment import Comment


class CommentRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, *, body: str, author_id: int, article_id: int) -> Comment:
        comment = Comment(body=body, author_id=author_id, article_id=article_id)
        self._session.add(comment)
        await self._session.flush()
        await self._session.refresh(comment, attribute_names=["author"])
        return comment

    async def list_by_article(self, article_id: int) -> list[Comment]:
        stmt = (
            select(Comment)
            .where(Comment.article_id == article_id)
            .options(selectinload(Comment.author))
            .order_by(Comment.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().unique().all())

    async def get_by_id(self, comment_id: int) -> Comment | None:
        stmt = (
            select(Comment)
            .where(Comment.id == comment_id)
            .options(selectinload(Comment.author))
        )
        result = await self._session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def delete(self, comment: Comment) -> None:
        await self._session.delete(comment)
        await self._session.flush()
