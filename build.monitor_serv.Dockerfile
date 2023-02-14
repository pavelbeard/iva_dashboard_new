### BUILDER ###
FROM python:3.11.1-slim-bullseye as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements/reqs-monitor-server.txt .
RUN python3.11 -m venv /opt/venv; apt update; apt install gcc build-essential -y
ENV PATH=/opt/venv/bin:$PATH
RUN pip3.11 install $(grep -ivE "pywin32" reqs-monitor-server.txt)

### FINAL ###
FROM python:3.11.1-slim-bullseye

RUN mkdir -p /home/monitor-server-app/; \
    addgroup --system monitor;  \
    adduser --system monitor;  \
    usermod -aG monitor monitor

COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

ENV APP_HOME=/home/monitor-server-app/web
RUN  apt update;  \
     apt install netcat-openbsd -y;  \
     mkdir $APP_HOME;  \
     mkdir $APP_HOME/logs; \
     mkdir $APP_HOME/staticfiles;  \
     mkdir -p /etc/iva_dashboard;

WORKDIR $APP_HOME

COPY monitor_serv $APP_HOME

RUN chown -R monitor:monitor $APP_HOME; chmod u+rwx -R $APP_HOME
USER monitor

ENTRYPOINT ["/home/monitor-server-app/web/entrypoint.sh"]

