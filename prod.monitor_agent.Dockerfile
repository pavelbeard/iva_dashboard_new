FROM pavelbeard/monitor-agent:v1.4

CMD ["uvicorn", "main:app", "--host", "2.0.96.1", "--port", "8000"]