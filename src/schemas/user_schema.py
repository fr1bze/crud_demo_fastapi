from typing import Optional

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
