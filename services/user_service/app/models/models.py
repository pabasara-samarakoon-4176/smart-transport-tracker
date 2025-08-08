from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    alerts = relationship("Alert", back_populates="user")

class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)

    buses = relationship("Bus", back_populates="route")
    
class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True, index=True)
    registration_no = Column(String, unique=True, nullable=False)
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)

    route = relationship("Route", back_populates="buses")
    locations = relationship("Location", back_populates="bus")
    alerts = relationship("Alert", back_populates="bus")

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    bus = relationship("Bus", back_populates="locations")
    alerts = relationship("Alert", back_populates="location")

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    radius_m = Column(Integer, nullable=False)
    alert_triggered = Column(Boolean, default=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="alerts")
    location = relationship("Location", back_populates="alerts")
    bus = relationship("Bus", back_populates="alerts")