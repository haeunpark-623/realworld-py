from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.db import get_db
from realworld.errors import InvalidToken
from realworld.models.user import User
from realworld.services.auth import AuthService

_TOKEN_PREFIX = "Token "


async def require_auth(
    authorization: str | None = Header(default=None, alias="Authorization"),
    session: AsyncSession = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith(_TOKEN_PREFIX):
        raise InvalidToken()
    token = authorization[len(_TOKEN_PREFIX):]
    if not token:
        raise InvalidToken()
    return await AuthService(session).get_current_user(token)
