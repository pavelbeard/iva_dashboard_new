FROM pavelbeard/monitor-server-frontend:v1.0

WORKDIR /app

USER root

COPY monitor_serv_frontend .

RUN chown -R monitor:monitor .; chmod u+rwx -R .
USER monitor

CMD ["npm", "start"]


