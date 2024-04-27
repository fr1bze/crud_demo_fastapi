from typing import Optional

from fastapi import Depends
from fastapi_users import IntegerIDMixin, BaseUserManager, models, FastAPIUsers
from starlette.requests import Request

from ..database import UserModel, get_users_db, auth_backend

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, id]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
            self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: models.UP, token: str, request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: models.UP, token: str, request: Optional[Request] = None
    ) -> None:
        print(f"Verification requested for the {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_users_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[UserModel, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
