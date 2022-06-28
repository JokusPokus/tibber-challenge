# syntax=docker/dockerfile:1
FROM python:3.8

ENV APP_HOME /app
ENV PORT 8080
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME
COPY . .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD gunicorn --bind :$PORT --workers 1 --threads 8 service.wsgi:application
