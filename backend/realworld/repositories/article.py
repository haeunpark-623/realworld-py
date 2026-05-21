from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from realworld.models.article import Article, Tag
from realworld.models.user import User


class ArticleRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_with_filters(
        self, *, limit: int = 20, offset: int = 0, author: str | None = None
    ) -> tuple[list[Article], int]:
        base_stmt = select(Article)
        count_stmt = select(func.count()).select_from(Article)
        if author is not None:
            base_stmt = base_stmt.join(User, Article.author_id == User.id).where(
                User.username == author
            )
            count_stmt = count_stmt.join(User, Article.author_id == User.id).where(
                User.username == author
            )
        stmt = (
            base_stmt.options(selectinload(Article.tags))
            .order_by(Article.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        articles = list(result.scalars().unique().all())
        total = (await self._session.execute(count_stmt)).scalar_one()
        return articles, int(total)

    async def get_by_slug(self, slug: str) -> Article | None:
        stmt = select(Article).where(Article.slug == slug).options(selectinload(Article.tags))
        result = await self._session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(Article.id).where(Article.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_or_create_tag(self, name: str) -> Tag:
        stmt = select(Tag).where(Tag.name == name)
        result = await self._session.execute(stmt)
        tag = result.scalar_one_or_none()
        if tag is None:
            tag = Tag(name=name)
            self._session.add(tag)
            await self._session.flush()
            await self._session.refresh(tag)
        return tag

    async def add(
        self,
        *,
        slug: str,
        title: str,
        description: str | None,
        body: str,
        author_id: int,
        tags: list[Tag],
    ) -> Article:
        article = Article(
            slug=slug,
            title=title,
            description=description,
            body=body,
            author_id=author_id,
        )
        article.tags = list(tags)
        self._session.add(article)
        await self._session.flush()
        await self._session.refresh(article, attribute_names=["author", "tags"])
        return article

    async def delete(self, article: Article) -> None:
        await self._session.delete(article)
        await self._session.flush()
