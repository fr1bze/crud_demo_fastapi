from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List
from pydantic import EmailStr
from ..schemas.user_schema import User, UserCreate
from ..database import UserModel


class UserRepository:
    async def get_user(self, user_id: int, session: AsyncSession) -> User:
        statement = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    async def get_users(self, async_session: AsyncSession) -> List[User]:
        statement = select(UserModel)
        result = await async_session.execute(statement)
        users = result.scalars().all()
        return users

    async def create_user(self, name: str, email: EmailStr, password: str, session: AsyncSession) -> User:
        db_user = UserModel(name=name, email=email, is_active=True, is_verified=False, is_superuser=False)
        db_user.hashed_password = db_user.get_password_hash(password)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def delete_user(self, user_id, session: AsyncSession) -> User:
        statement = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()
        if user:
            await session.delete(user)
            await session.commit()
        return user
