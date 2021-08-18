import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, TIMESTAMP, Boolean

from app.db.base_class import Base


class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    altitude = Column(Float)
    is_valid = Column(Boolean)
    received_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

