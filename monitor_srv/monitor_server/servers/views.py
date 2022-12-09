from django.http import HttpResponse
from django.shortcuts import render

from .mixins import ServerMixin


# Create your views here.


def index(request):
    return HttpResponse("hello world!")


class ServerServicesStates(ServerMixin):
    template_name = "servers_service_status_all.html"
    context_object_name = "servers"
    monitor_url = "http://localhost:8000/api/monitor/services-status-all"
    targets = {"192.168.248.4"}


class ServerSystemctlStatus(ServerMixin):
    template_name = "servers_systemctl.html"
    context_object_name = "servers"
    monitor_url = "http://localhost:8000/api/monitor/systemctl-services"
    targets = {"192.168.248.4"}