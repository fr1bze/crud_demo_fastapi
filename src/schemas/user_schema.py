from pydantic import BaseModel, Emailstr

class UserBase(BaseModel):
    username: str
    email: Emailstr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True