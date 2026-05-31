from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.db import get_db
from realworld.deps.auth import require_auth
from realworld.models.article import Article
from realworld.models.user import User
from realworld.schemas.article import (
    ArticleCreateRequest,
    ArticleResponse,
    ArticlesListResponse,
    ArticleUpdateRequest,
    ArticleView,
    ProfileEmbed,
)
from realworld.services.article import ArticleService

router = APIRouter(prefix="/api/articles", tags=["articles"])


def _to_view(article: Article) -> ArticleView:
    return ArticleView(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
        tag_list=[tag.name for tag in article.tags],
        created_at=article.created_at,
        updated_at=article.updated_at,
        author=ProfileEmbed(username=article.author.username),
    )


@router.get("", response_model=ArticlesListResponse, response_model_by_alias=True)
async def list_articles(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    author: str | None = None,
    tag: str | None = None,
    session: AsyncSession = Depends(get_db),
) -> ArticlesListResponse:
    service = ArticleService(session)
    articles, total = await service.list(limit=limit, offset=offset, author=author, tag=tag)
    return ArticlesListResponse(articles=[_to_view(a) for a in articles], articles_count=total)


@router.get("/{slug}", response_model=ArticleResponse, response_model_by_alias=True)
async def get_article(slug: str, session: AsyncSession = Depends(get_db)) -> ArticleResponse:
    service = ArticleService(session)
    article = await service.get_by_slug(slug)
    return ArticleResponse(article=_to_view(article))


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleResponse,
    response_model_by_alias=True,
)
async def create_article(
    payload: ArticleCreateRequest,
    user: User = Depends(require_auth),
    session: AsyncSession = Depends(get_db),
) -> ArticleResponse:
    service = ArticleService(session)
    article = await service.create(
        author_id=user.id,
        title=payload.article.title,
        description=payload.article.description,
        body=payload.article.body,
        tag_list=payload.article.tag_list,
    )
    await session.commit()
    return ArticleResponse(article=_to_view(article))


@router.put("/{slug}", response_model=ArticleResponse, response_model_by_alias=True)
async def update_article(
    slug: str,
    payload: ArticleUpdateRequest,
    user: User = Depends(require_auth),
    session: AsyncSession = Depends(get_db),
) -> ArticleResponse:
    service = ArticleService(session)
    article = await service.update(
        slug=slug,
        author_id=user.id,
        title=payload.article.title,
        description=payload.article.description,
        body=payload.article.body,
        tag_list=payload.article.tag_list,
    )
    await session.commit()
    return ArticleResponse(article=_to_view(article))


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    slug: str,
    user: User = Depends(require_auth),
    session: AsyncSession = Depends(get_db),
) -> Response:
    service = ArticleService(session)
    await service.delete(slug=slug, author_id=user.id)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
