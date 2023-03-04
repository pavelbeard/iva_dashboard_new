FROM pavelbeard/monitor-agent:v1.9

ENV APP_HOME=/home/monitor-agent-app/monitor_agent
WORKDIR $APP_HOME

COPY monitor_agent $APP_HOME

RUN chown -R monitor:monitor $APP_HOME; chmod u+rwx -R $APP_HOME
USER monitor



