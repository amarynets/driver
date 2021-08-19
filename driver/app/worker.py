import json

from celery import Celery
from celery.utils.log import get_task_logger

from app.config import settings
from app.db import SessionLocal
from app.models import Position
from app.schema import Position as PositionSchema
from app.service import prepare_position

celery_app = Celery('tasks', broker='pyamqp://guest@rabbit//')
logger = get_task_logger(__name__)


@celery_app.task
def handle_position(position):
    db = SessionLocal()
    position = PositionSchema(**json.loads(position))
    last_driver_position = db.query(Position).filter_by(driver_id=position.driver_id).order_by(
        Position.id.desc()).limit(1).first()
    position = prepare_position(position, last_driver_position, settings)
    position = Position(
        driver_id=position.driver_id,
        latitude=position.latitude,
        longitude=position.longitude,
        speed=position.speed,
        altitude=position.altitude,
        displacement_speed=position.displacement_speed,
        is_valid=position.is_valid,
        received_at=position.received_at
    )
    db.add(position)
    db.commit()