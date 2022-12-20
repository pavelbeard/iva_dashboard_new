### BUILDER ###
FROM python:3.11.1-alpine3.16 as builder

WORKDIR /usr/src/app

COPY reqs-monitor-agent.txt .
RUN pip3.11 wheel \
    --no-cache-dir \
    --no-deps \
    --wheel-dir /usr/src/app/wheels -r reqs-monitor-agent.txt

### FINAL ###
FROM python:3.11.1-alpine3.16

#RUN apk add openssl; \
#    mkdir -p /home/monitor-agent-app/; addgroup -S monitor; adduser -S monitor -G monitor;


COPY --from=builder /usr/src/app/wheels /wheels
RUN apk add openssl; pip3.11 install --no-cache /wheels/*

ENV HOME=/home/monitor-agent-app/
ENV APP_HOME=/home/monitor-agent-app/api
RUN mkdir $APP_HOME; mkdir $APP_HOME/logs; rm -rf /wheels

WORKDIR $APP_HOME

COPY . $APP_HOME

#RUN chown -R monitor:monitor $APP_HOME
#USER monitor
