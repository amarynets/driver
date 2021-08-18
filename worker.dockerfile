FROM python:3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./driver/app /app

ENV PYTHONPATH=/app

CMD ["celery", "--app=app.worker.celery_app", "worker", "-c", "2", "--loglevel=info"]