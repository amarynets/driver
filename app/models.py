from sqlalchemy import Column, ForeignKey, Integer, String, Float
import geoalchemy2

from app.db.base_class import Base


class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Integer)
    altitude = Column(Integer)

