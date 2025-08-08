from fastapi import FastAPI
from app.models import User
from database import engine
from app.routers.users import router as user_router

from routers.users import router as user_router

User.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)