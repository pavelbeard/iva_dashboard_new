from django.shortcuts import render
from .logic import IvaMetricsHandler
from . import mixins
from . import models

# Create your views here.


def index_view(request):
    targets = models.Target.objects.all()
    addresses = [f"{target.address}:{target.port}" for target in targets]
    return render(request=request, template_name="index.html", context={"addresses": addresses})


class Processes(mixins.ServersInfoMixin):
    cmd = "uname -n && service --status-all"
    callback_iva_metrics_handler = IvaMetricsHandler.service_status_all


class CPU(mixins.ServersInfoMixin):
    cmd = "uname -n && echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')] && lscpu | egrep 'CPU\(s\):'"
    callback_iva_metrics_handler = IvaMetricsHandler.cpu_utilization

