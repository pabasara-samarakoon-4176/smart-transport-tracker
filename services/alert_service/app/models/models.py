from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base
from datetime import datetime

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, nullable=False)
    location_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    radius_m = Column(Integer, nullable=False)
    alert_triggered = Column(Boolean, default=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=False)