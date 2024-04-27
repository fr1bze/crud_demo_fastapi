from fastapi_users import schemas


class User(schemas.BaseUser[int]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    name: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
