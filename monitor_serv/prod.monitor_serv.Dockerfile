FROM pavelbeard/monitor-server:v1.3

COPY monitor_serv_assemble_files/server-config.yml /etc/iva_dashboard/server-config.yml

COPY . .

CMD ["uvicorn", "monitor_serv.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
ENTRYPOINT ["/home/monitor-server-app/web/entrypoint.sh"]
