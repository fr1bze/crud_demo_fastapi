from sqlalchemy.orm import Session
from typing import List
from ..schemas.user_schema import User
from .. import schemas


class UserRepository:
    def get_user(self, id) -> User:
        pass
    
    def get_users(self) -> List[User]:
        pass

    def create_user(self) -> User:
        pass

    def delete_user(self, id):
        pass
