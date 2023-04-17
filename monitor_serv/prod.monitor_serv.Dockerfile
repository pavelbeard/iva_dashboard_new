FROM pavelbeard/prod.monitor-server:v0.7

ENV APP_HOME=/home/monitor-server-app/web
WORKDIR $APP_HOME

USER root

COPY . $APP_HOME

EXPOSE 8040

RUN chown -R monitor:monitor $APP_HOME; chmod u+rwx -R $APP_HOME
USER monitor



