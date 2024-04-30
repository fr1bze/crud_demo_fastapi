from fastapi_users import schemas
from pydantic import BaseModel


class User(schemas.BaseUser[int]):
    name: str
    roles: str


class UserCreate(schemas.BaseUserCreate):
    name: str
    roles: str


class UserUpdate(schemas.BaseUserUpdate):
    pass

class Role(BaseModel):
    role_name: str