from fastapi import FastAPI
from app.database import engine
from app.models import Base 
from app.routers.bus import router as bus_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(bus_router)