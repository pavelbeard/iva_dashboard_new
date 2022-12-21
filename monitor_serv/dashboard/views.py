from django.shortcuts import render
from .logic import IvaMetricsHandler
from . import mixins
from . import models


# Create your views here.


def index_view(request):
    targets = models.Target.objects.all()
    addresses = [f"{target.address}:{target.port}" for target in targets]
    return render(request=request, template_name="index.html", context={"addresses": addresses})


class Processes(mixins.ServerAnalysisMixin):
    cmd = "uname -n && /usr/sbin/service --status-all"
    callback_iva_metrics_handler = IvaMetricsHandler.exec_analysis


class CPU(mixins.ServerAnalysisMixin):
    # cmd = "echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')] && lscpu | egrep 'CPU\(s\):'"
    cmd = "uname -n && cat /proc/stat "
    callback_iva_metrics_handler = IvaMetricsHandler.cpu_analysis


class RAM(mixins.ServerAnalysisMixin):
    cmd = "uname -n && free -k"
    callback_iva_metrics_handler = IvaMetricsHandler.ram_analysis


class DiskSpace(mixins.ServerAnalysisMixin):
    cmd = "uname -n && df -h"
    callback_iva_metrics_handler = IvaMetricsHandler.file_sys_analysis


class Uptime(mixins.ServerAnalysisMixin):
    cmd = "uname -n && "
