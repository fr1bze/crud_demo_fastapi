from fastapi import FastAPI
from .controllers.user_controller import router

app = FastAPI()

app.include_router(router=router)