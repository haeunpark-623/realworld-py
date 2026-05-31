from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.db import get_db
from realworld.repositories.article import ArticleRepo
from realworld.schemas.tag import TagsListResponse

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("", response_model=TagsListResponse)
async def list_tags(session: AsyncSession = Depends(get_db)) -> TagsListResponse:
    names = await ArticleRepo(session).list_all_tag_names()
    return TagsListResponse(tags=names)
