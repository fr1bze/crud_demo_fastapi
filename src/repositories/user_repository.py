from sqlalchemy.orm import Session
from typing import List
from src.schemas.user_schema import User
from src.models.user_model import UserModel


class UserRepository:
    def get_user(self, id: int, session: Session) -> User:
        return session.query(UserModel).filter(User.id == id).first()
    
    def get_users(self) -> List[User]:
        pass

    def create_user(self, name: str, email: str, session: Session) -> User:
        db_user = UserModel(name=name, email=email)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return User(name=db_user.username, email=db_user.email)

    def delete_user(self, id, session: Session):
        user = session.query(UserModel).filter(User.id == id).first()
        if user:
            session.delete(user)
            session.commit()
