from fastapi import FastAPI
import models
from database import engine

from routers.bus import router as bus_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(bus_router)