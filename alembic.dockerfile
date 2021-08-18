FROM python:3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY driver /app
ENV PYTHONPATH=/app
WORKDIR /app

# CMD ["ls", "-la"]
CMD ["alembic", "upgrade", "head"]