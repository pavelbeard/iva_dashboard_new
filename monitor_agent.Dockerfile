FROM python:3.11.1-slim-bullseye

WORKDIR /app

COPY packages/monitor-agent-packages/ /app

RUN pip install $(ls); rm *

EXPOSE 8000/tcp

CMD uvicorn main:app --reload --host 2.0.96.1 --port 8000