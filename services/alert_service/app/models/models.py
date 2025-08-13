from sqlalchemy import Column, Float, Integer, String, DateTime, Boolean
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

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    route_id = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True, index=True)
    registration_no = Column(String, unique=True, nullable=False)
    route_id = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)