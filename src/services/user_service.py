from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import User, Role
from ..database import UserModel

class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_users(self, session: AsyncSession) -> List[User]:
        return await self.repository.get_users(session)

    async def get_user(self, user_id: int, session: AsyncSession) -> User:
        return await self.repository.get_user(user_id, session)

    async def create_user(self, name: str, email: str, password: str, roles: str, session: AsyncSession) -> User:
        return await self.repository.create_user(name, email, password, roles, session)

    async def delete_user(self, user_id: int, session: AsyncSession) -> User:
        return await self.repository.delete_user(user_id, session)

    async def get_role_by_name(self, role_name: str, session: AsyncSession) -> Optional[Role]:
        return await self.repository.get_role_by_name(role_name, session)

    async def assign_role_to_user(self, user_id: int, role_id: int, session: AsyncSession) -> None:
        await self.repository.assign_role_to_user(user_id, role_id, session)
