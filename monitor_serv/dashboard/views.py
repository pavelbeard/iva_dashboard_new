import json

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control

from . import mixins
from . import models

# Create your views.py here.

app_version = settings.APP_VERSION
mail_to = settings.MAIL_TO_DEV
call_to = settings.CALL_TO_DEV


def index_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:dashboard"))
    else:

        storage = get_messages(request)

        if len(storage) == 0:
            messages.info(request, "Войдите в систему чтобы увидеть Инфопанель")

    return render(
        request=request,
        template_name="base/2_index.html",
        context={"app_version": app_version, "index": True, "mail_to": mail_to, "call_to": call_to}
    )


@login_required(login_url=reverse_lazy("dashboard_users:login"))
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_view(request):
    query = models.Target.objects.filter(is_being_scan=True)
    targets = [
        {
            "address": f"{target.address}:{target.port}",
            "id": f"{target.address.replace('.', '')}{target.port}",
            "role": target.server_role
        }
        for target in query
    ]
    return render(
        request=request,
        template_name="base/4_dashboard.html",
        context={"targets": targets, "app_version": app_version, "mon_agent_available": True}
    )


def dashboard_monitor_unavailable(request):
    return render(
        request=request,
        template_name="base/4_dashboard.html",
        context={"app_version": app_version}
    )


class Processes(mixins.ServerAnalysisMixin):
    cmd = "/usr/sbin/service --status-all"


class CPUTop(mixins.ServerAnalysisMixin):
    model = models.CPU
    template_name = "dashboard/parts/1_server.html"
    cmd = 'top -bn 1 -d.2 | grep "Cpu" && top 1 -w 70 -bn 1 | grep -P "^(%)"'


class RAM(mixins.ServerAnalysisMixin):
    model = models.RAM
    cmd = "free -kh --si"


class DiskSpace(mixins.ServerAnalysisMixin):
    # на продакт сервере нужно заменить команду du sh на sudo du -sh.
    # для других разработчиков на будущее: лучше давать права админа на выполнение команд мониторинга
    # или перемещать эти утилиты в другие группы
    #
    # UPD: дано разрешение выполнять команду du без прав админа: sudo chmod +s $(which du)
    # UPD: "du -sh --exclude=mnt --exclude=proc /" - не используется из-за огромной нагрузки на процессор
    model = models.DiskSpace
    cmd = 'df -h && lsblk | grep -E "^sda"'


class Net(mixins.ServerAnalysisMixin):
    model = models.NetInterface
    cmd = "/usr/sbin/ifconfig"


class Uptime(mixins.ServerAnalysisMixin):
    cmd = "uname -n && uptime"


def get_interval(request):
    """Возвращает интервал снятия метрик в секундах"""
    try:
        dboard_settings = models.DashboardSettings.objects.get(command_id=1)
        interval = dboard_settings.scrape_interval
        return http.JsonResponse(json.dumps({"interval": interval}), safe=False)
    except models.DashboardSettings.DoesNotExist:
        http.JsonResponse(json.dumps({"SettingsObjectNotFound": "no data."}), safe=False)


class ServerData(mixins.ServerAnalysisMixin):
    model = models.Target
    cmd = "uname -n && uname -r && cat /etc/os-release"
