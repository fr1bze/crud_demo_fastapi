from fastapi import APIRouter, Depends, Path, Field
from pydantic import EmailStr
from typing import List
from sqlalchemy.orm import Session
from ..depends import get_user_service
from ..schemas.user_schema import User
from ..services.user_service import UserService
from ..database import SessionLocal, get_db

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
async def get_all_users(user_id: int,
                        user_service: UserService = Depends(get_user_service)
                        ) -> User:
    user = user_service.get_user(user_id)
    return user


@router.post(
    "",
    responses={400: {"description": "Bad request"}},
    response_model=User,
    description="User creating",
)
async def create_user(
        name: str = Path(min_length=3, max_length=20),
        email: EmailStr = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$'),
        session: Session = Depends(get_db),
        user_service: UserService = Depends(get_user_service),
) -> User:
    user = user_service.create_user(name, email, session)
    return user
