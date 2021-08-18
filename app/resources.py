import math
import datetime
from fastapi import APIRouter
import haversine as hs

from app.schema import Position as PositionSchema
from app.models import Position


from app.db.session import SessionLocal
from app.config import settings

router = APIRouter()


@router.post('/positions', response_model=PositionSchema)
def upload_position(position: PositionSchema):
    db = SessionLocal()
    if not position.received_at:
        position.received_at = datetime.datetime.utcnow()
    if position.speed > settings.MAX_SPEED:
        is_valid = False
    elif position.altitude > settings.MAX_ALTITUDE:
        is_valid = False
    else:
        # TODO: Move to DB side with GIS
        # TODO: Use cache for last position
        # TODO: Maybe count only valid position
        last_driver_position = db.query(Position).filter_by(driver_id=position.driver_id).order_by(
            Position.id.desc()).limit(1).first()
        if last_driver_position:
            displacement = hs.haversine((position.latitude, position.longitude), (last_driver_position.latitude, last_driver_position.longitude))
            if displacement == 0 and position.speed != 0:
                # Car stay on the same place
                is_valid = False
            else:
                time = position.received_at - last_driver_position.received_at
                calculated_speed = displacement / time.seconds * 3600
                if calculated_speed > settings.MAX_SPEED:
                    is_valid = False
                else:
                    is_valid = True
        else:
            is_valid = True

    position = Position(
        driver_id=position.driver_id,
        latitude=position.latitude,
        longitude=position.longitude,
        speed=position.speed,
        altitude=position.altitude,
        is_valid=is_valid,
        received_at=position.received_at
    )
    db.add(position)
    db.commit()

