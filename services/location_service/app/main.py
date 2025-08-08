from fastapi import FastAPI
import models
from database import engine

from routers.location_tracking import router as location_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(location_router)