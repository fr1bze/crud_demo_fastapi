from fastapi import FastAPI
from src.controllers import *
from src.controllers import *
from src.controllers.user_controller import router

app = FastAPI()

app.include_router(router=router)