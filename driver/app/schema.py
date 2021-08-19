from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Position(BaseModel):
    id: Optional[int]
    driver_id: int
    latitude: float
    longitude: float
    speed: float
    altitude: float
    displacement_speed: Optional[float] = None
    is_valid: Optional[bool]
    received_at: Optional[datetime] = None

    class Config:
        orm_mode = True
