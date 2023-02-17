FROM pavelbeard/monitor-agent:v1.7

CMD ["uvicorn", "monitor_agent.main:app", "--host", "2.0.96.1", "--port", "8000"]