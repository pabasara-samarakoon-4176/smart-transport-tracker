from fastapi import FastAPI
from app.database import engine
from app.models import Base 
from app.routers.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)