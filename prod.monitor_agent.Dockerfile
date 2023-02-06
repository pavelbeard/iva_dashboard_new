FROM pavelbeard/monitor-agent:v1.3

CMD ["uvicorn", "main:app", "--host", "2.0.96.1", "--port", "8000"]