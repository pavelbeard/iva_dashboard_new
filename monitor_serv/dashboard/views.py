import json

import yaml
from django import http
from django.shortcuts import render
from django.conf import settings
from logic import IvaMetricsHandler
from . import mixins
from . import models


# Create your views here.


def index_view(request):
    app_version = settings.APPLICATION_VERSION
    targets = models.Target.objects.all()
    addresses = [{"address": f"{target.address}:{target.port}", "role": target.server_role} for target in targets]
    return render(request=request, template_name="index.html", context={
        "addresses": addresses, "app_version": app_version
    })


class Processes(mixins.ServerAnalysisMixin):
    cmd = "uname -n && /usr/sbin/service --status-all"
    callback_iva_metrics_handler = IvaMetricsHandler.exec_analysis


class CPU(mixins.ServerAnalysisMixin):
    # cmd = "echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')] && lscpu | egrep 'CPU\(s\):'"
    cmd = 'uname -n && top -bn 1 | grep -P "^(%)" && top 1 -w 70 -bn 1 | grep -P "^(%)"'
    callback_iva_metrics_handler = IvaMetricsHandler.cpu_analysis


class RAM(mixins.ServerAnalysisMixin):
    cmd = "uname -n && free -k"
    callback_iva_metrics_handler = IvaMetricsHandler.ram_analysis


class DiskSpace(mixins.ServerAnalysisMixin):
    # на продакт сервере нужно заменить команду du sh на sudo du -sh.
    # для других разработчиков на будущее: лучше давать права админа на выполнение команд мониторинга
    # или перемещать эти утилиты в другие группы
    #
    # UPD: дано разрешение выполнять команду du без прав админа: sudo chmod +s $(which du)
    # UPD: "du -sh --exclude=mnt --exclude=proc /" - не используется из-за огромной нагрузки на процессор
    cmd = 'uname -n && df -h && lsblk | grep -E "^sda"'
    callback_iva_metrics_handler = IvaMetricsHandler.file_sys_analysis


class Net(mixins.ServerAnalysisMixin):
    cmd = "uname -n && /usr/sbin/ifconfig"
    callback_iva_metrics_handler = IvaMetricsHandler.net_analysis


class Uptime(mixins.ServerAnalysisMixin):
    cmd = "uname -n && uptime"
    callback_iva_metrics_handler = IvaMetricsHandler.uptime


def get_interval(request):
    try:
        server_config_file = settings.SERVER_CONFIG_FILE
        with open(server_config_file, 'r') as file:
            config = yaml.safe_load(file)
            interval = config.get('settings').get('interval')
            return http.JsonResponse(json.dumps({"interval": interval}), safe=False)
    except FileNotFoundError:
        http.JsonResponse(json.dumps({"file_not_found": "no data."}), safe=False)
