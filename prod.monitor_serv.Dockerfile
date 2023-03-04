FROM pavelbeard/monitor-server:v1.8

ENV APP_HOME=/home/monitor-server-app/web
WORKDIR $APP_HOME

COPY monitor_serv $APP_HOME

RUN chown -R monitor:monitor $APP_HOME; chmod u+rwx -R $APP_HOME
USER monitor



