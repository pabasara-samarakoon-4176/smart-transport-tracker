from fastapi import FastAPI
from app.database import engine
from app.models import Base 
from app.routers.users import router as user_router
from app.database import engine, Base
from app.models.models import User
from fastapi.middleware.cors import CORSMiddleware
import os

Base.metadata.drop_all(bind=engine, tables=[User.__table__])
Base.metadata.create_all(bind=engine, tables=[User.__table__])

origins = os.getenv("CORS_ORIGINS", "").split(",")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],
)
app.include_router(user_router)