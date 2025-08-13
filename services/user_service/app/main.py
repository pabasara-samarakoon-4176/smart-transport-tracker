from fastapi import FastAPI
from app.database import engine
from app.models import Base 
from app.routers.users import router as user_router
from app.database import engine, Base
from app.models.models import User

Base.metadata.drop_all(bind=engine, tables=[User.__table__])
Base.metadata.create_all(bind=engine, tables=[User.__table__])

app = FastAPI()
app.include_router(user_router)