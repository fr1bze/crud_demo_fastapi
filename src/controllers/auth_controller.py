from fastapi import Cookie, APIRouter, Depends, HTTPException, Header
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi.responses import JSONResponse

from src.database import UserModel, get_async_session, TokenTable
from src.schemas.token_schema import requestdetails, TokenSchema
from src.schemas.user_schema import User
from src.utils import create_access_token, create_refresh_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "SECRET"
JWT_REFRESH_SECRET_KEY = "SECRET"


@auth_router.post('/login', response_model=TokenSchema)
async def login(request: requestdetails, db: AsyncSession = Depends(get_async_session)):

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

    response = JSONResponse(
        {"access_token": access, "refresh_token": refresh, "message": "You've been successfully logged in"})
    response.set_cookie("token", value=access)

    token_db = TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    db.add(token_db)
    await db.commit()
    await db.refresh(token_db)

    return response


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str = Header(...), db: AsyncSession = Depends(get_async_session)):

    token_db = await db.execute(select(TokenTable).filter(TokenTable.access_token == token))
    token_db = token_db.scalars().first()

    if token_db:
        token_db.status = False
        await db.commit()
        await db.execute(delete(TokenTable).where(TokenTable.access_token==token))
        return {"message": "You have been successfully logged out."}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token.")


async def get_current_token(token: str = Cookie(None)):
    return token


async def get_current_user(token: str = Depends(get_current_token), session: AsyncSession = Depends(get_async_session)):
    statement = await session.execute(select(TokenTable).filter(TokenTable.access_token == token))
    token_value = statement.scalars().first()
    if not token_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token.")

    #debug
    print("Token", token_value)
    statement = await session.execute(select(UserModel).filter(UserModel.id == token_value.user_id))
    user = statement.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user


@auth_router.get("/private")
async def get_private_endpoint(current_token: str = Depends(get_current_token)):
    return {"token": current_token}

@auth_router.get("/authenticated-route")
async def authenticated_route(user: UserModel = Depends(get_current_user)):
    return {"message": f"Hello, {user.name}!"}