from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models import models
from app.schemas import schemas

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

@router.post("/", response_model=schemas.BusResponse)
def create_bus(bus: schemas.BusCreate, db: Session = Depends(get_db)):
    db_bus = models.Bus(**bus.dict())
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus

@router.put("/{bus_id}", response_model=schemas.BusResponse)
def update_bus(bus_id: int, bus: schemas.BusUpdate, db: Session = Depends(get_db)):
    db_bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    for key, value in bus.dict(exclude_unset=True).items():
        setattr(db_bus, key, value)
    
    db.commit()
    db.refresh(db_bus)
    return db_bus

@router.delete("/{bus_id}", response_model=schemas.BusResponse)
def delete_bus(bus_id: int, db: Session = Depends(get_db)):
    db_bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    db.delete(db_bus)
    db.commit()
    return db_bus