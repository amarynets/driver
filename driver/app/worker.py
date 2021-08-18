import datetime
import json

from celery import Celery
from celery.utils.log import get_task_logger
import haversine as hs

from app.config import settings
from app.db import SessionLocal
from app.models import Position
from app.schema import Position as PositionSchema

celery_app = Celery('tasks', broker='pyamqp://guest@rabbit//')
logger = get_task_logger(__name__)


@celery_app.task
def handle_position(position):
    db = SessionLocal()
    position = PositionSchema(**json.loads(position))
    calculated_speed = 0
    if not position.received_at:
        position.received_at = datetime.datetime.utcnow()
    if position.speed > settings.MAX_SPEED:
        is_valid = False
        logger.warning(f'Driver: {position.driver_id} has higher speed({position.speed}) than max allowed({settings.MAX_SPEED})')
    elif position.altitude > settings.MAX_ALTITUDE:
        is_valid = False
        logger.warning(f'Driver: {position.driver_id} has higher altutude({position.altitude}) than max allowed({settings.MAX_ALTITUDE})')
    else:
        last_driver_position = db.query(Position).filter_by(driver_id=position.driver_id).order_by(
            Position.id.desc()).limit(1).first()
        if last_driver_position:
            displacement = hs.haversine((position.latitude, position.longitude),
                                        (last_driver_position.latitude, last_driver_position.longitude))
            time = position.received_at - last_driver_position.received_at
            calculated_speed = displacement / time.seconds * 3600
            if displacement == 0 and position.speed != 0:
                # Car stay on the same place
                is_valid = False
                logger.warning(f'Driver: {position.driver_id} is not moving, but speed is not 0')
            else:

                if calculated_speed > settings.MAX_SPEED:
                    is_valid = False
                    logger.warning(f'Driver: {position.driver_id} moved from coordinates{(last_driver_position.latitude, last_driver_position.longitude)}'
                                   f' to {(position.latitude, position.longitude)}, time({time}), displacement({displacement}) with speed({calculated_speed}), allowed spped({settings.MAX_SPEED})')
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
        calculated_speed=calculated_speed,
        is_valid=is_valid,
        received_at=position.received_at
    )
    db.add(position)
    db.commit()
