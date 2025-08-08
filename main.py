from fastapi import FastAPI
import models
from database import engine

from routers.users import router as user_router
from routers.bus import router as bus_router
from routers.routes import router as route_router
from routers.location_tracking import router as location_router
from routers.alerts import router as alert_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(bus_router)
app.include_router(route_router)
app.include_router(location_router)
app.include_router(alert_router)