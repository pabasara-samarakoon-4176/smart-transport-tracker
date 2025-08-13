from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BusBase(BaseModel):
    registration_no: str
    route_id: int
    latitude: float
    longitude: float
    timestamp: datetime

class trackingSchema(BaseModel):
    id: int
    latitude: float
    longitude: float

class BusCreate(BusBase):
    pass

class BusUpdate(BaseModel):
    registration_no: Optional[str] = None
    route_id: Optional[int] = None

class BusResponse(BusBase):
    id: int

    class Config:
        orm_mode = True
