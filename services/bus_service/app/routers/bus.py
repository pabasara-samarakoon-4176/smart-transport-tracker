from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.kafka.producer import send_bus_created_event, send_bus_location_event
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(
    prefix="/buses",
    tags=["buses"]
)

@router.post("/")
def create_bus(bus: schemas.BusCreate, db: Session = Depends(get_db)):
    db_bus = models.Bus(**bus.dict())
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    send_bus_created_event({
        "id": db_bus.id,
        "registration_no": db_bus.registration_no,
        "route_id": db_bus.route_id,
        "latitude": db_bus.latitude,
        "longitude": db_bus.longitude
    })

    return {
        "id": db_bus.id,
        "registration_no": db_bus.registration_no,
        "message": "Bus registered successfully."
    }

@router.put("/track")
def track_bus(bus_data: schemas.trackingSchema, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_data.id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    bus.latitude = bus_data.latitude
    bus.longitude = bus_data.longitude

    db.commit()
    db.refresh(bus)

    send_bus_location_event({
        "id": bus.id,
        "latitude": bus.latitude,
        "longitude": bus.longitude
    })

    return {
        "message": "Bus location updated successfully",
        "bus_id": bus.id,
        "latitude": bus.latitude,
        "longitude": bus.longitude,
        "timestamp": datetime.utcnow()
    }