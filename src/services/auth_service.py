from fastapi import APIRouter, Cookie
from starlette.responses import JSONResponse

router = APIRouter()

@router.post("/login")
async def user_login():
    response = JSONResponse({"message": "Login successful"})
    response.set_cookie(key="auth_token", value="your_token_value")
    return response

@router.get("/logout")
async def user_logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie(key="auth_token")
    return response