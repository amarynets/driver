import datetime
from fastapi import APIRouter
import haversine as hs

from app.schema import Position as PositionSchema
from app.models import Position


from app.db.session import SessionLocal
from app.config import settings
from app.worker import handle_position

router = APIRouter()


@router.post('/positions')
def upload_position(position: PositionSchema):
    position.received_at = datetime.datetime.utcnow()
    handle_position.delay(position.json())
    return {'status': 200}


@router.get('/health-check')
def health_check():
    try:
        db = SessionLocal()
        db.execute('SELECT 1;')
        db_alive = True
    except Exception as e:
        db_alive = False
    return {
        'db_alive': db_alive
    }

