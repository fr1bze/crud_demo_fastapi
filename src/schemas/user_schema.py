# from sqlalchemy import Session
# from .. import repositories, schemas

# def get_user(db: Session, user_id: int):
#     return repositories.get_user(db=db, user_id=user_id)
# def create_user(db: Session, user: schemas.):    
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True