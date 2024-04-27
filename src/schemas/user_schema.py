from typing import Optional
from pydantic import BaseModel, constr
from pydantic.v1 import validator


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(BaseModel):
    name: str
    email: constr(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: constr(min_length=8)

    @validator('password')
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters length")
        return v


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
