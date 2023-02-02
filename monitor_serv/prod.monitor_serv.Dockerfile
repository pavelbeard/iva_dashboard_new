FROM pavelbeard/monitor-server:v1.3

COPY . .

CMD ["uvicorn", "monitor_serv.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
ENTRYPOINT ["/home/monitor-server-app/web/entrypoint.sh"]
