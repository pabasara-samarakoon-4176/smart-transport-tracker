from pydantic import BaseModel
from datetime import datetime

class RegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    route_id: int
    latitude: float
    longitude: float
    timestamp: datetime

class LoginSchema(BaseModel):
    email: str
    password: str

class trackingSchema(BaseModel):
    id: int
    latitude: float
    longitude: float
    timestamp: datetime