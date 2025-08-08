from typing import Optional
from pydantic import BaseModel

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
