from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import Field
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from ..depends import get_user_service
from ..schemas.user_schema import User, UserCreate
from ..services.user_service import UserService
from ..database import async_session_maker, get_users_db, UserModel, pwd_context

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    responses={400: {"description": "Bad request"}},
    response_model=List[User],
    description="Listing of all users"
)
async def get_all_users(
        session: AsyncSession = Depends(get_users_db),
        user_service: UserService = Depends(get_user_service)
) -> List[User]:
    users = await user_service.get_users(session)
    if not users:
        return []
    return users


@router.get(
    "/{user_id}",
    responses={400: {"description": "Bad request"}},
    response_model=User,
    description="Listing of all users"
)
async def get_user(user_id: int,
                   session: AsyncSession = Depends(get_users_db),
                   user_service: UserService = Depends(get_user_service)
                   ) -> User:
    user = await user_service.get_user(user_id, session)
    return user


@router.post(
    "",
    responses={400: {"description": "Bad request"}},
    response_model=User,
    description="Create a new user",
)
async def create_user(
    request: UserCreate,
    session: AsyncSession = Depends(get_users_db),
    user_service: UserService = Depends(get_user_service)
) -> User:
    user = await user_service.create_user(request.name, request.email, request.password, session)
    return user

@router.delete(
    "/{user_id}",
    responses={404: {"description": "User not found"}},
    description="Deletes user by ID"
)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_users_db),
        user_service: UserService = Depends(get_user_service)
        ) -> User:
    user = await user_service.get_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_service.delete_user(user_id, session)
    return user