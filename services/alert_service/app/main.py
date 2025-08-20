from fastapi import FastAPI
from app.database import engine, Base
from app.models.models import Alert
from fastapi.middleware.cors import CORSMiddleware
from app.routers.alerts import router as alert_router
import os

Base.metadata.create_all(bind=engine)

origins = os.getenv("CORS_ORIGINS", "").split(",")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],
)
app.include_router(alert_router)