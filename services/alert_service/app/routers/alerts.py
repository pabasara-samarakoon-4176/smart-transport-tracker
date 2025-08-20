from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.get("/{user_id}")
def get_user_alerts(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Alert).filter(models.Alert.user_id == user_id).all()