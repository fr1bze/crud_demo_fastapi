from typing import Optional

from fastapi import Depends
from fastapi_users import IntegerIDMixin, BaseUserManager, models, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from starlette.requests import Request

from src.database import cookie_transport
from ..database import UserModel, get_users_db, auth_backend, get_jwt_strategy

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, id]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
            self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has registered.")

async def get_user_manager(user_db=Depends(get_users_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[UserModel, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


