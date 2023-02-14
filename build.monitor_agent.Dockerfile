### BUILDER ###
FROM python:3.11.1-alpine3.16 as builder

WORKDIR /usr/src/app

COPY requirements/reqs-monitor-agent.txt .
RUN pip3.11 wheel \
    --no-cache-dir \
    --no-deps \
    --wheel-dir /usr/src/app/wheels $(grep -ivE "pyreadline3|pywin32|pyparsing" reqs-monitor-agent.txt)

### FINAL ###
FROM python:3.11.1-alpine3.16

RUN apk add openssl; \
    mkdir -p /home/monitor-agent-app/; addgroup -S monitor; adduser -S monitor -G monitor;


COPY --from=builder /usr/src/app/wheels /wheels
RUN apk add openssl; pip3.11 install --no-cache /wheels/*; rm -rf /wheels

ENV HOME=/home/monitor-agent-app/
ENV APP_HOME=/home/monitor-agent-app/monitor_agent
RUN mkdir -p $APP_HOME; mkdir -p $APP_HOME/logs;

WORKDIR $HOME

COPY monitor_agent $APP_HOME

RUN chown -R monitor:monitor $APP_HOME; chmod u+rwx -R $APP_HOME
USER monitor
