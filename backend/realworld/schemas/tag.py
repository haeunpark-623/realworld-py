from pydantic import BaseModel


class TagsListResponse(BaseModel):
    tags: list[str]
