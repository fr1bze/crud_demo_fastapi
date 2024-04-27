from fastapi import FastAPI
from .controllers.user_controller import router
from fastapi_users.authentication import CookieTransport

cookie_transport = CookieTransport(cookie_max_age=3600)

app = FastAPI()

app.include_router(router=router)