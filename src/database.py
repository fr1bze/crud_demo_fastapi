from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from passlib.context import CryptContext

SQLALCHEMY_DATABASE_USER_URL = "sqlite+aiosqlite:///users.db"
SQLALCHEMY_DATABASE_ROLE_URL = "sqlite+aiosqlite:///roles.db"

SECRET = "SECRET"
Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def get_password_hash(self, password) -> str:
        return pwd_context.hash(password)

engine = create_async_engine(SQLALCHEMY_DATABASE_USER_URL, echo=True)

async_session_maker = sessionmaker(autocommit=False, class_=AsyncSession, bind=engine)

async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def get_users_db(session: AsyncSession = Depends(get_async_session)):
    yield session


cookie_transport = CookieTransport(cookie_path="auth/jwt/login", cookie_max_age=3600)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


from .rsa_key import generate_rsa_keys

private, public = generate_rsa_keys()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=private,
        lifetime_seconds=3600,
        algorithm="RS256",
        public_key=public
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
