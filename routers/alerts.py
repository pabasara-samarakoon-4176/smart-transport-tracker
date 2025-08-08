from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from datetime import datetime

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.post("/")
def create_alert(
    bus_id: int, 
    location_id: int, 
    radius_m: int, 
    alert_triggered: bool, 
    triggered_at: datetime,
    message: str, 
    user_id: int,
    db: Session = Depends(get_db)):
    alert = models.Alert(
        bus_id=bus_id,
        location_id=location_id,
        radius_m=radius_m,
        alert_triggered=alert_triggered,
        triggered_at=triggered_at or datetime.utcnow(),
        message=message,
        user_id=user_id
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.post("/check/{bus_id}", response_model=schemas.AlertStatus)
def check_alert_condition(bus_id: int, db: Session = Depends(get_db)):
    location = db.query(models.Location).filter(models.Location.bus_id == bus_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found for the bus")
    
    should_trigger = location.latitude < 7.0

    alert = db.query(models.Alert).filter(
        models.Alert.bus_id == bus_id,
        models.Alert.message == "Soon arrival"
    ).first()

    if should_trigger:
        if not alert:
            alert = models.Alert(
                bus_id=bus_id,
                alert_type="arrival_soon",
                alert_triggered=True,
                triggered_at=datetime.utcnow()
            )
            db.add(alert)
        else:
            alert.alert_triggered = True
            alert.triggered_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
        return alert
    
    if not alert:
        alert = models.Alert(
            bus_id=bus_id,
            alert_type="arrival_soon",
            alert_triggered=False
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)

    return alert

@router.get("/{bus_id}")
def get_alerts(bus_id: int, db: Session = Depends(get_db)):
    return db.query(models.Alert).filter(models.Alert.bus_id == bus_id).all()

@router.get("/user/{user_id}")
def get_user_alerts(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Alert).filter(models.Alert.user_id == user_id).all()

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if alert:
        db.delete(alert)
        db.commit()
        return {"message": "Alert deleted successfully"}
    return {"message": "Alert not found"}, 404

@router.put("/{alert_id}")
def update_alert(
    alert_id: int, 
    bus_id: int = None, 
    location_id: int = None, 
    radius_m: int = None, 
    alert_triggered: bool = None, 
    triggered_at: datetime = None,
    message: str = None, 
    user_id: int = None,
    db: Session = Depends(get_db)):
    
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        return {"message": "Alert not found"}, 404
    
    if bus_id is not None:
        alert.bus_id = bus_id
    if location_id is not None:
        alert.location_id = location_id
    if radius_m is not None:
        alert.radius_m = radius_m
    if alert_triggered is not None:
        alert.alert_triggered = alert_triggered
    if triggered_at is not None:
        alert.triggered_at = triggered_at
    if message is not None:
        alert.message = message
    if user_id is not None:
        alert.user_id = user_id
    
    db.commit()
    db.refresh(alert)
    return alert

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if alert:
        db.delete(alert)
        db.commit()
        return {"message": "Alert deleted successfully"}
    return {"message": "Alert not found"}, 404