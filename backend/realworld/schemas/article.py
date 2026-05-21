from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProfileEmbed(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    bio: str | None = None
    image: str | None = None


class ArticleCreatePayload(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    body: str = Field(min_length=1)
    tag_list: list[str] = Field(default_factory=list, alias="tagList", max_length=20)


class ArticleUpdatePayload(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    body: str | None = Field(default=None, min_length=1)
    tag_list: list[str] | None = Field(default=None, alias="tagList", max_length=20)


class ArticleCreateRequest(BaseModel):
    article: ArticleCreatePayload


class ArticleUpdateRequest(BaseModel):
    article: ArticleUpdatePayload


class ArticleView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str
    title: str
    description: str | None
    body: str
    tag_list: list[str] = Field(serialization_alias="tagList")
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")
    author: ProfileEmbed


class ArticleResponse(BaseModel):
    article: ArticleView


class ArticlesListResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    articles: list[ArticleView]
    articles_count: int = Field(serialization_alias="articlesCount")
