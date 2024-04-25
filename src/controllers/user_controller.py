from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.depends import get_user_service
from src.schemas.user_schema import User
from src.services.user_service import UserService
from src.database import SessionLocal, get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "",
    responses={400: {"description": "Bad request"}},
    response_model=List[User],
    description="Listing of all users"
)

async def get_all_users(
    user_service: UserService = Depends(get_user_service)
) -> List[User]:
    users = user_service.get_users()
    return users

@router.get(
    "/{user_id}",
    responses={400: {"description": "Bad request"}},
    response_model=List[User],
    description="Listing of all users"
)

async def get_all_users(id:int,
    user_service: UserService = Depends(get_user_service)
) -> User:
    user = user_service.get_user(id)
    return user


@router.post(
    "",
    responses={400: {"description": "Bad request"}},
    response_model=User,
    description="User creating",
)
async def create_user(
        name: str,
        email: str,
        session: Session = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
) -> User:
    user = user_service.create_user(name, email, session)
    return user