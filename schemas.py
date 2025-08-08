from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BusBase(BaseModel):
    registration_no: str
    route_id: int

class BusCreate(BusBase):
    pass

class BusUpdate(BaseModel):
    registration_no: Optional[str] = None
    route_id: Optional[int] = None

class BusResponse(BusBase):
    id: int

    class Config:
        orm_mode = True

class RegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

class LocationResponse(BaseModel):
    bus_id: int
    latitude: float
    longitude: float
    updated_at: datetime

    class Config:
        orm_mode = True

class AlertStatus(BaseModel):
    bus_id: int
    location_id: int
    radius_m: int
    alert_triggered: bool
    triggered_at: datetime
    message: str
    user_id: int

    class Config:
        orm_mode = True