from fastapi import APIRouter

router = APIRouter()


@router.get('/drivers')
async def drivers():
    return {'drivers': []}


@router.post('/positions')
async def upload_position():
    pass

