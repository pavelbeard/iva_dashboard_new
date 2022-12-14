from django.views import generic
from monitor_srv.monitor_server.servers.logic import IvaMetricsHandler
from .mixins import ServerInfoMixin
from . import models


# Create your views here.


class ServerProcesses(ServerInfoMixin):
    cmd = "uname -n && service --status-all"
    cb_handler = IvaMetricsHandler.service_status_all
