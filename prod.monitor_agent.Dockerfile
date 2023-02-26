FROM pavelbeard/monitor-agent:v1.7


ENTRYPOINT ["python3.11", "/home/monitor-agent-app/monitor_agent/entrypoint.py"]

