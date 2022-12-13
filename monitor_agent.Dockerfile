FROM python:3.11.1-slim-bullseye

WORKDIR /app

COPY
COPY monitor_agent/reqs.txt /app

RUN pip install $(grep -ivE "pywin32" reqs.txt)

EXPOSE 8000/tcp

CMD uvicorn main:app --reload --host 2.0.96.1 --port 8000