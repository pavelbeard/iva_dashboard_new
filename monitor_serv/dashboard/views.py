from django.shortcuts import render
from .logic import IvaMetricsHandler
from . import mixins
from . import models


# Create your views here.


def index_view(request):
    targets = models.Target.objects.all()
    addresses = [{"address": f"{target.address}:{target.port}", "role": target.server_role} for target in targets]
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
    # на продакт сервере нужно заменить команду du sh на sudo du -sh.
    # для других разработчиков на будущее: лучше давать права админа на выполнение команд мониторинга
    # или перемещать эти утилиты в другие группы
    #
    # UPD: дано разрешение выполнять команду du без прав админа: sudo chmod +s $(which du)
    cmd = 'uname -n && df -h && lsblk | grep -E "^sda" && du -sh --exclude=mnt --exclude=proc /'
    callback_iva_metrics_handler = IvaMetricsHandler.file_sys_analysis


class Net(mixins.ServerAnalysisMixin):
    # команды iftop может не быть на целевой машине, проверить перед
    # развертыванием дашборда, установить в случае отсутствия
    # UPD: дано разрешение выполнять команду iftop без прав админа: sudo chmod +s $(which /usr/sbin/iftop)
    cmd = "uname -n && /usr/sbin/iftop -t -s 1 -P"
    callback_iva_metrics_handler = IvaMetricsHandler.net_analysis


class Uptime(mixins.ServerAnalysisMixin):
    cmd = "uname -n && uptime"
    callback_iva_metrics_handler = IvaMetricsHandler.uptime
