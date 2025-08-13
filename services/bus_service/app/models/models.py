from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base
    
class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True, index=True)
    registration_no = Column(String, unique=True, nullable=False)
    route_id = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)