FROM python:3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./driver/position_generator.py /app/position_generator.py
WORKDIR /app

CMD ["python3", "position_generator.py"]