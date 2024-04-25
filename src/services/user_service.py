from typing import List
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import User
from ..models.user_model import UserModel

class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def get_users(self) -> List[User]:
        return self.repository.get_users()

    async def get_user(self, id: int) -> User:
        return self.repository.get_user(id)

    def create_user(self, name: str, email: EmailStr, session: Session) -> User:
        return self.repository.create_user(name, email, session)
