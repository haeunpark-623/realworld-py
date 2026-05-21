from pydantic import BaseModel, EmailStr, Field


class UserCreatePayload(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLoginPayload(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserCreateRequest(BaseModel):
    user: UserCreatePayload


class UserLoginRequest(BaseModel):
    user: UserLoginPayload


class UserView(BaseModel):
    username: str
    email: EmailStr
    token: str
    bio: str | None = None
    image: str | None = None


class UserResponse(BaseModel):
    user: UserView
