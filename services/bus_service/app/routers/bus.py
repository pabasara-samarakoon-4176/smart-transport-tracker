from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.kafka.producer import send_bus_created_event
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.kafka.tracking_producer import send_bus_location_event
import os
from dotenv import load_dotenv

load_dotenv()
KAFKA_USER_TOPIC = os.getenv("KAFKA_USER_TOPIC", "bus-events")

router = APIRouter(
    prefix="/buses",
    tags=["buses"]
)

@router.get("/", response_model=list[schemas.BusResponse])
def read_buses(db: Session = Depends(get_db)):
    return db.query(models.Bus).all()

@router.get("/{bus_id}", response_model=schemas.BusResponse)
def read_bus(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus

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

# @router.put("/{bus_id}", response_model=schemas.BusResponse)
# def update_bus(bus_id: int, bus: schemas.BusUpdate, db: Session = Depends(get_db)):
#     db_bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
#     if not db_bus:
#         raise HTTPException(status_code=404, detail="Bus not found")
    
#     for key, value in bus.dict(exclude_unset=True).items():
#         setattr(db_bus, key, value)
    
#     db.commit()
#     db.refresh(db_bus)
#     return db_bus

@router.delete("/{bus_id}", response_model=schemas.BusResponse)
def delete_bus(bus_id: int, db: Session = Depends(get_db)):
    db_bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    db.delete(db_bus)
    db.commit()
    return db_bus

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