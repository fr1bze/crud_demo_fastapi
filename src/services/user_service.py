from typing import List

from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import User

class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def get_users(self) -> List[User]:
        return self.repository.get_users()

    def createe_user(self) -> User:
        return self.repository.create_user() 