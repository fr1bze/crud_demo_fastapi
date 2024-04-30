from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from src.auth.user_manager import current_active_user, get_user_manager
from src.controllers.auth_controller import auth_router
from src.database import UserModel, create_db_and_tables, auth_backend
from src.schemas.user_schema import User
from src.controllers.user_controller import router
from fastapi_users.authentication import CookieTransport

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

cookie_transport = CookieTransport(cookie_max_age=3600)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

app.include_router(router=router)
app.include_router(router=auth_router)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
