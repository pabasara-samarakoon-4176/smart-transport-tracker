from fastapi import FastAPI
import models
from database import engine

from routers.alerts import router as alert_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(alert_router)