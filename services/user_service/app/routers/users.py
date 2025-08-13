from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas import schemas
from passlib.context import CryptContext
from app.kafka.producer import send_user_created_event
from app.kafka.tracking_producer import send_user_location_event
import os
from dotenv import load_dotenv

load_dotenv()
KAFKA_USER_TOPIC = os.getenv("KAFKA_USER_TOPIC", "user-events")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register_user(user_data: schemas.RegisterSchema, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user_data.password)

    new_user = models.User(
        name=user_data.name,
        phone=user_data.phone,
        email=user_data.email,
        password=hashed_password,
        route_id=user_data.route_id,
        latitude=user_data.latitude,
        longitude=user_data.longitude,
        timestamp=user_data.timestamp
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_user_created_event({
        "id": new_user.id, 
        "name": new_user.name,
        "phone": new_user.phone,
        "email": new_user.email,
        "route_id": new_user.route_id,
        "latitude": new_user.latitude,
        "longitude": new_user.longitude,
        # "timestamp": new_user.timestamp
    })

    return {"message": "User registered successfully.", "user_id": new_user.id}

@router.put("/track")
def track_user(user_data: schemas.trackingSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_data.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.latitude = user_data.latitude
    user.longitude = user_data.longitude
    user.last_tracked_at = user_data.timestamp or datetime.utcnow()

    db.commit()
    db.refresh(user)

    send_user_location_event({
        "id": user.id,
        "latitude": user.latitude,
        "longitude": user.longitude,
        "timestamp": user.last_tracked_at.isoformat()
    })

    return {
        "message": "User location updated successfully",
        "user_id": user.id,
        "latitude": user.latitude,
        "longitude": user.longitude,
        "timestamp": user.last_tracked_at
    }

@router.post("/login")
def login_user(user_data: schemas.LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    return {"message": "Login successful", "user_id": user.id}