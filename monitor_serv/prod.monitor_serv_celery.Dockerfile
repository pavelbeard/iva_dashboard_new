FROM pavelbeard/prod.monitor-serv-worker:v1.0
ENV WORKER_HOME=/home/celery-worker/
WORKDIR $WORKER_HOME

USER root

COPY . $WORKER_HOME

RUN chown -R monitor-celery:monitor-celery $WORKER_HOME; chmod u+rwx -R $WORKER_HOME
USER monitor-celery
