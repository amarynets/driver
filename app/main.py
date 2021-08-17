from fastapi import FastAPI

from config import settings
from resources import router

app = FastAPI(
    title=settings.APP_NAME, openapi_url="/openapi.json"
)


@app.get('/')
def home():
    return {
        'APP': settings.APP_NAME
    }


app.include_router(router)
