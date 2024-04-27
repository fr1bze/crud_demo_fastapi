from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from ..auth.user_manager import get_user_manager
from ..database import UserModel, auth_backend
from ..schemas.user_schema import UserCreate, User

fastapi_users = FastAPIUsers[UserModel, id](
    get_user_manager,
    [auth_backend],
)

auth_router = {"router": fastapi_users.get_auth_router(auth_backend),
               "prefix": "/auth/jwt",
               "tags": ["auth"],
               }

register_router = {"router": fastapi_users.get_register_router(User, UserCreate),
               "prefix": "/auth",
               "tags": ["auth"],
               }
reset_pass_router = {"router": fastapi_users.get_reset_password_router(),
               "prefix": "/auth",
               "tags": ["auth"],
               }
verify_router = {"router": fastapi_users.get_verify_router(User),
               "prefix": "/auth",
               "tags": ["auth"],
               }

