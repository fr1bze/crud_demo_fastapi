import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List, Optional
from pydantic import EmailStr
from ..schemas.user_schema import User, UserCreate
from ..database import UserModel, RoleModel


class UserRepository:
    async def get_users(self, async_session: AsyncSession) -> List[User]:
        statement = select(UserModel).options(joinedload(UserModel.roles))
        result = await async_session.execute(statement)

        users = result.unique().all()

        user_objects = [User(
            id=user[0].id,
            name=user[0].name,
            email=user[0].email,
            hashed_password=user[0].hashed_password,
            is_active=user[0].is_active,
            is_superuser=user[0].is_superuser,
            is_verified=user[0].is_verified,
            roles=", ".join([role.name for role in user[0].roles]) if user[0].roles else ""
        ) for user in users]

        return user_objects
        return []


    async def create_user(self, name: str, email: str, password: str, roles: str, session: AsyncSession) -> User:
        existing_user = await session.execute(select(UserModel).filter(UserModel.email == email))
        existing_user = existing_user.scalars().first()
        if existing_user:
            raise ValueError("Email address already in use")

        hashed_password = UserModel.get_password_hash(password)
        user = UserModel(name=name, email=email, hashed_password=hashed_password)

        role = await session.execute(select(RoleModel).filter(RoleModel.name == roles))
        role = role.scalars().first()
        if role:
            user.roles.append(role)

        session.add(user)
        await session.commit()

        return user

    async def get_user(self, user_id: int, session: AsyncSession) -> User:
        statement = select(UserModel).filter(UserModel.id == user_id).options(selectinload(UserModel.roles))
        result = await session.execute(statement)
        user = result.scalars().first()

        if user:
            user_object = User(
                id=user.id,
                name=user.name,
                email=user.email,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                is_verified=user.is_verified,
                roles=", ".join([role.name for role in user.roles]) if user.roles else ""
            )
            return user_object
        else:
            raise ValueError(f"User with id {user_id} not found")


    async def delete_user(self, user_id: int, session: AsyncSession) -> Optional[User]:
        statement = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()
        logger = logging.getLogger()
        logger.info(f"User {user} deleted")

        if user:
            user_object = User(
                id=user.id,
                name=user.name,
                email=user.email,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                is_verified=user.is_verified,
                roles=", ".join([role.name for role in user.roles]) if user.roles else ""
            )
            await session.delete(user)
            await session.commit()

            return user_object
        else:
            return None
    async def get_role_by_name(self, role_name: str, session: AsyncSession) -> Optional[RoleModel]:
        async with session as async_session:
            role = await async_session.execute(select(RoleModel).filter(RoleModel.name == role_name))
            return role.scalar()

    async def assign_role_to_user(self, user_id: int, role: int, session: AsyncSession) -> UserModel:
        async with session as async_session:
            user = await async_session.get(UserModel, user_id)
            if user:
                user.roles.append(role)
                await async_session.commit()
                return user
            else:
                return None
