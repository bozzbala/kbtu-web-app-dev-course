FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput