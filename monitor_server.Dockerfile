FROM python:3.11.1-slim-bullseye

WORKDIR /app

COPY monitor_srv/etc /etc/iva_dashboard
COPY packages/monitor-server-packages/ /app

RUN apt update; apt install build-essential -y; pip install $(ls); rm *;

CMD uvicorn monitor_server.asgi:application --host 2.0.96.3 --port 8000 --reload