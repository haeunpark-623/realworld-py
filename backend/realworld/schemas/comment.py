from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from realworld.schemas.article import ProfileEmbed


class CommentCreatePayload(BaseModel):
    body: str = Field(min_length=1)


class CommentUpdatePayload(BaseModel):
    body: str = Field(min_length=1)


class CommentCreateRequest(BaseModel):
    comment: CommentCreatePayload


class CommentUpdateRequest(BaseModel):
    comment: CommentUpdatePayload


class CommentView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    body: str
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")
    author: ProfileEmbed


class CommentResponse(BaseModel):
    comment: CommentView


class CommentsListResponse(BaseModel):
    comments: list[CommentView]
