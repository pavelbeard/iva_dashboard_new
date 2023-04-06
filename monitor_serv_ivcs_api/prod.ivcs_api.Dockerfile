FROM pavelbeard/prod.ivcs-api:v0.1

ENV APP_HOME=/home/ivcs-api/web
WORKDIR $APP_HOME

USER root

COPY . $APP_HOME

EXPOSE 8040

RUN chown -R ivcs:ivcs $APP_HOME; chmod u+rwx -R $APP_HOME
USER ivcs



