from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from realworld.errors import Forbidden, NotFound
from realworld.models.article import Article
from realworld.repositories.article import ArticleRepo
from realworld.utils.slug import slugify, unique_slug


class ArticleService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._articles = ArticleRepo(session)

    async def list(
        self, *, limit: int = 20, offset: int = 0, author: str | None = None
    ) -> tuple[list[Article], int]:
        return await self._articles.list_with_filters(
            limit=limit, offset=offset, author=author
        )

    async def get_by_slug(self, slug: str) -> Article:
        article = await self._articles.get_by_slug(slug)
        if article is None:
            raise NotFound("게시글을 찾을 수 없습니다")
        return article

    async def create(
        self,
        *,
        author_id: int,
        title: str,
        description: str | None,
        body: str,
        tag_list: list[str],
    ) -> Article:
        base = slugify(title)
        slug = await unique_slug(self._articles, base)
        tags = [await self._articles.get_or_create_tag(name) for name in tag_list]
        return await self._articles.add(
            slug=slug,
            title=title,
            description=description,
            body=body,
            author_id=author_id,
            tags=tags,
        )

    async def update(
        self,
        *,
        slug: str,
        author_id: int,
        title: str | None,
        description: str | None,
        body: str | None,
        tag_list: list[str] | None,
    ) -> Article:
        article = await self.get_by_slug(slug)
        if article.author_id != author_id:
            raise Forbidden()
        if title is not None:
            article.title = title
        if description is not None:
            article.description = description
        if body is not None:
            article.body = body
        if tag_list is not None:
            article.tags = [
                await self._articles.get_or_create_tag(name) for name in tag_list
            ]
        await self._session.flush()
        await self._session.refresh(article, attribute_names=["author", "tags"])
        return article

    async def delete(self, *, slug: str, author_id: int) -> None:
        article = await self.get_by_slug(slug)
        if article.author_id != author_id:
            raise Forbidden()
        await self._articles.delete(article)
