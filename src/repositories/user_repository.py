from sqlalchemy.orm import Session
from typing import List
from pydantic import EmailStr
from ..schemas.user_schema import User
from ..database import UserModel


class UserRepository:
    def get_user(self, id: int, session: Session) -> User:
        return session.query(UserModel).filter(UserModel.id == id).first()
    
    def get_users(self, session: Session) -> List[User]:
        return session.query(UserModel).all()

    def create_user(self, name: str, email: EmailStr, session: Session) -> User:
        db_user = UserModel(name=name, email=email)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def delete_user(self, id, session: Session) -> User:
        user = session.query(UserModel).filter(UserModel.id == id).first()
        if user:
            session.delete(user)
            session.commit()
        return user
