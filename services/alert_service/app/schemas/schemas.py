from datetime import datetime
from pydantic import BaseModel

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