from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import Session

from passlib.context import CryptContext


SQLALCHEMY_DATABASE_USER_URL = "sqlite:///users.db"

SQLALCHEMY_DATABASE_ROLE_URL = "sqlite:///roles.db"

engine = create_engine(SQLALCHEMY_DATABASE_USER_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class RoleModel(Base):
#     __tablename__ = 'roles'
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     user = relationship('UserModel', secondary='user_roles', backref="users")

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True, index=True)

    hashed_password = Column(String)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def get_password_hash(self, password) -> str:
        return pwd_context.hash(password)


    # role = relationship('RoleModel', secondary="user_roles", backref="roles")


Base.metadata.create_all(engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

