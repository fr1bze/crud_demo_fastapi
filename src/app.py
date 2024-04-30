from fastapi import FastAPI, Depends

from .auth.user_manager import current_active_user
from .controllers.auth_controller import auth_router
from .database import UserModel, create_db_and_tables
from .schemas.user_schema import User
from .controllers.user_controller import router
from fastapi_users.authentication import CookieTransport

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

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

# app.include_router(router=register_router["router"],
#                    prefix=register_router["prefix"],
#                    tags=register_router["tags"],
#                    )
#
# app.include_router(router=reset_pass_router["router"],
#                    prefix=reset_pass_router["prefix"],
#                    tags=reset_pass_router["tags"],
#                    )
#
# app.include_router(router=verify_router["router"],
#                    prefix=verify_router["prefix"],
#                    tags=verify_router["tags"],
#                    )


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.name}"}


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
