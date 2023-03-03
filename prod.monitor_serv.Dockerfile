FROM pavelbeard/monitor-server:v1.8

COPY monitor_serv .

RUN chown -R monitor:monitor $APP_HOME; chmod u+rwx -R $APP_HOME
USER monitor



