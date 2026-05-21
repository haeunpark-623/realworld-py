from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.db import get_db
from realworld.deps.auth import require_auth
from realworld.models.comment import Comment
from realworld.models.user import User
from realworld.schemas.article import ProfileEmbed
from realworld.schemas.comment import (
    CommentCreateRequest,
    CommentResponse,
    CommentsListResponse,
    CommentUpdateRequest,
    CommentView,
)
from realworld.services.comment import CommentService

router = APIRouter(prefix="/api/articles", tags=["comments"])


def _to_view(comment: Comment) -> CommentView:
    return CommentView(
        id=comment.id,
        body=comment.body,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        author=ProfileEmbed(username=comment.author.username),
    )


@router.get("/{slug}/comments", response_model=CommentsListResponse, response_model_by_alias=True)
async def list_comments(slug: str, session: AsyncSession = Depends(get_db)) -> CommentsListResponse:
    service = CommentService(session)
    comments = await service.list_by_article(slug)
    return CommentsListResponse(comments=[_to_view(c) for c in comments])


@router.post(
    "/{slug}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
    response_model_by_alias=True,
)
async def create_comment(
    slug: str,
    payload: CommentCreateRequest,
    user: User = Depends(require_auth),
    session: AsyncSession = Depends(get_db),
) -> CommentResponse:
    service = CommentService(session)
    comment = await service.create(slug=slug, author_id=user.id, body=payload.comment.body)
    await session.commit()
    return CommentResponse(comment=_to_view(comment))


@router.put(
    "/{slug}/comments/{comment_id}",
    response_model=CommentResponse,
    response_model_by_alias=True,
)
async def update_comment(
    slug: str,
    comment_id: int,
    payload: CommentUpdateRequest,
    user: User = Depends(require_auth),
    session: AsyncSession = Depends(get_db),
) -> CommentResponse:
    service = CommentService(session)
    comment = await service.update(
        slug=slug, comment_id=comment_id, author_id=user.id, body=payload.comment.body
    )
    await session.commit()
    return CommentResponse(comment=_to_view(comment))


@router.delete("/{slug}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    slug: str,
    comment_id: int,
    user: User = Depends(require_auth),
    session: AsyncSession = Depends(get_db),
) -> Response:
    service = CommentService(session)
    await service.delete(slug=slug, comment_id=comment_id, author_id=user.id)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
