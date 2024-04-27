from typing import List
from sqlalchemy.orm import Session

from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import User
from ..database import UserModel

class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_users(self, session: Session) -> List[User]:
        return self.repository.get_users(session)

    async def get_user(self, user_id: int, session: Session) -> User:
        return self.repository.get_user(user_id, session)

    async def create_user(self, name: str, email: str, password: str, session: Session) -> User:
        return self.repository.create_user(name, email, password, session)

    async def delete_user(self, user_id: int, session: Session) -> User:
        return self.repository.delete_user(user_id,session)
