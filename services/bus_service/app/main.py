from fastapi import FastAPI
from app.database import engine
from app.models import Base 
from app.models.models import Bus
from app.routers.bus import router as bus_router

Base.metadata.drop_all(bind=engine, tables=[Bus.__table__])
Base.metadata.create_all(bind=engine, tables=[Bus.__table__])

app = FastAPI()

app.include_router(bus_router)