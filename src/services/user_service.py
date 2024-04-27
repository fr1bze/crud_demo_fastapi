from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import User
from ..database import UserModel

class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_users(self, session: AsyncSession) -> List[User]:
        return await self.repository.get_users(session)

    async def get_user(self, user_id: int, session: AsyncSession) -> User:
        return await self.repository.get_user(user_id, session)

    async def create_user(self, name: str, email: str, password: str, session: AsyncSession) -> User:
        created_user = await self.repository.create_user(name, email, password, session)
        return created_user

    async def delete_user(self, user_id: int, session: AsyncSession) -> User:
        return await self.repository.delete_user(user_id, session)
