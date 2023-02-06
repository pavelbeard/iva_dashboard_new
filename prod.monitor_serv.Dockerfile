FROM pavelbeard/monitor-server:v1.4

CMD ["uvicorn", "monitor_serv.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["/home/monitor-server-app/web/entrypoint.sh"]
