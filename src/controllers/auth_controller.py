from fastapi import Cookie, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import manager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse, HTMLResponse

from src.schemas import token_schema
from src.database import UserModel, get_async_session, TokenTable
from src.schemas.token_schema import requestdetails, TokenSchema
from src.utils import create_access_token, create_refresh_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


last_access_token = None

@auth_router.post('/login', response_model=TokenSchema)
async def login(request: requestdetails, db: AsyncSession = Depends(get_async_session)):
    global last_access_token

    print(request.email, request.password)
    statement = select(UserModel).filter(UserModel.email == request.email)
    result = await db.execute(statement)

    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    last_access_token = access

    token_db = TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    db.add(token_db)
    await db.commit()
    await db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(db: AsyncSession = Depends(get_async_session)):
    global last_access_token

    if last_access_token:
        token_db = await db.execute(select(TokenTable).filter(TokenTable.access_token == last_access_token))
        token_db = token_db.scalars().first()

        if token_db:
            token_db.status = False
            await db.commit()
            last_access_token = None  # Сбрасываем последний использованный токен
            return {"message": "You have been successfully logged out."}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token.")

#
# @auth_router.get("/private")
# async def get_private_endpoint(current_user: UserModel = Depends(get_current_user)):
#     return "You are an authenticated user"