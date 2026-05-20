from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from realworld.models.user import User


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, username: str, email: str, password_hash: str) -> User:
        user = User(username=username, email=email, password_hash=password_hash)
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user
