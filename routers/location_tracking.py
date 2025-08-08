from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from datetime import datetime

router = APIRouter(
    prefix="/location_tracking",
    tags=["location_tracking"]
)

@router.post("/update/{bus_id}", response_model=schemas.LocationResponse)
def update_location(bus_id: int, location: schemas.LocationUpdate, db: Session = Depends(get_db)):
    db_bus = db.query(models.Bus).filter(
        models.Bus.id == bus_id
    ).first()
    if not db_bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    db_location = db.query(models.Location).filter(models.Location.bus_id == bus_id).first()

    if db_location:
        db_location.latitude = location.latitude
        db_location.longitude = location.longitude
        db_location.updated_at = datetime.utcnow()
    else:
        db_location = models.Location(
            bus_id=bus_id,
            latitude=location.latitude,
            longitude=location.longitude
        )
        db.add(db_location)

    db.commit()
    db.refresh(db_location)
    return db_location

@router.get("/{bus_id}")
def get_latest_location(bus_id: int, db: Session = Depends(get_db)):
    loc = db.query(models.Location).filter(models.Location.bus_id == bus_id)\
            .order_by(models.Location.timestamp.desc()).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found.")
    return loc

@router.get("/latest")
def get_all_latest_locations(db: Session = Depends(get_db)):
    locations = db.query(models.Location).order_by(models.Location.timestamp.desc()).all()
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found.")
    return locations

@router.get("/history/{bus_id}/history?start={start}&end={end}")
def get_location_history(bus_id: int, start: datetime, end: datetime, db: Session = Depends(get_db)):
    history = db.query(models.Location).filter(
        models.Location.bus_id == bus_id,
        models.Location.timestamp >= start,
        models.Location.timestamp <= end
    ).order_by(models.Location.timestamp).all()
    
    if not history:
        raise HTTPException(status_code=404, detail="No location history found for this bus.")
    
    return history