from django.shortcuts import render
from .logic import IvaMetricsHandler
from . import mixins

# Create your views here.


class Processes(mixins.ServersInfoMixin):
    cmd = "uname -n && service --status-all"
    callback_iva_metrics_handler = IvaMetricsHandler.service_status_all


class CPU(mixins.ServersInfoMixin):
    cmd = "uname -n && service --status-all"
    callback_iva_metrics_handler = IvaMetricsHandler.service_status_all
