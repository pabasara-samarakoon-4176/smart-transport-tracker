from fastapi import FastAPI
from app.models import models
from app.database import engine

from app.routers.alerts import router as alert_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(alert_router)