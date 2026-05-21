from sqlalchemy.ext.asyncio import AsyncSession

from realworld.errors import (
    DuplicateEmail,
    DuplicateUsername,
    InvalidCredentials,
    InvalidToken,
)
from realworld.models.user import User
from realworld.repositories.user import UserRepo
from realworld.utils.jwt import decode_token, encode_token
from realworld.utils.security import hash_password, verify_password


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._users = UserRepo(session)

    async def register(self, username: str, email: str, password: str) -> User:
        if await self._users.find_by_email(email) is not None:
            raise DuplicateEmail()
        if await self._users.find_by_username(username) is not None:
            raise DuplicateUsername()
        return await self._users.create(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )

    async def authenticate(self, email: str, password: str) -> str:
        user = await self._users.find_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentials()
        return encode_token(user.id)

    async def get_current_user(self, token: str) -> User:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise InvalidToken()
        try:
            user_id = int(sub)
        except (TypeError, ValueError) as exc:
            raise InvalidToken() from exc
        user = await self._users.find_by_id(user_id)
        if user is None:
            raise InvalidToken()
        return user
