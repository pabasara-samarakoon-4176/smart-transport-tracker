from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/routes",
    tags=["routes"]
)

@router.post("/")
def create_route(name: str, origin: str, destination: str, db: Session = Depends(get_db)):
    route = models.Route(name=name, origin=origin, destination=destination)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

@router.get("/")
def list_routes(db: Session = Depends(get_db)):
    return db.query(models.Route).all()

@router.get("/{route_id}")
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.put("/{route_id}")
def update_route(route_id: int, name: str, origin: str, destination: str, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    route.name = name
    route.origin = origin
    route.destination = destination
    db.commit()
    db.refresh(route)
    return route

@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    db.delete(route)
    db.commit()
    return {"detail": "Route deleted successfully"}