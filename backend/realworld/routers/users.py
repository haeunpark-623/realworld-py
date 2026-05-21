from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.db import get_db
from realworld.deps.auth import require_auth
from realworld.models.user import User
from realworld.schemas.user import (
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
    UserView,
)
from realworld.services.auth import AuthService
from realworld.utils.jwt import encode_token

router = APIRouter(prefix="/api", tags=["users"])


def _to_view(user: User, token: str) -> UserView:
    return UserView(
        username=user.username,
        email=user.email,
        token=token,
        bio=None,
        image=None,
    )


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    payload: UserCreateRequest, session: AsyncSession = Depends(get_db)
) -> UserResponse:
    service = AuthService(session)
    user = await service.register(
        username=payload.user.username,
        email=payload.user.email,
        password=payload.user.password,
    )
    await session.commit()
    token = encode_token(user.id)
    return UserResponse(user=_to_view(user, token))


@router.post("/users/login", response_model=UserResponse)
async def login(payload: UserLoginRequest, session: AsyncSession = Depends(get_db)) -> UserResponse:
    service = AuthService(session)
    token = await service.authenticate(payload.user.email, payload.user.password)
    user = await service.get_current_user(token)
    return UserResponse(user=_to_view(user, token))


@router.get("/user", response_model=UserResponse)
async def current_user(user: User = Depends(require_auth)) -> UserResponse:
    token = encode_token(user.id)
    return UserResponse(user=_to_view(user, token))
