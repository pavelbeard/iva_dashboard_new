# monitor_serv_celery
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor_serv.settings")

app = Celery("monitor_serv")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(packages=("api", "dashboard", "dashboard_ivcs"))


@app.task
def debug_task():
    return {"ok": "ok"}