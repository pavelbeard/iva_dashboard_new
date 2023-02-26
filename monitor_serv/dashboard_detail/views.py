from core_logic.views import AppVersionMixin, ContextDataFromImporterMixin
from dashboard.models import CPU, RAM, DiskSpace, NetInterface
from django.views.generic import TemplateView

from monitor_serv import settings

# Create your views.py here.

APP_VERSION = settings.APP_VERSION


class CPUDetailView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = CPU
    template_name = "dashboard_detail/2_cpu.html"
    app_version = APP_VERSION


class RAMDetailView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = RAM
    template_name = "dashboard_detail/3_ram.html"
    app_version = APP_VERSION


class DiskSpaceDetailView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = DiskSpace
    template_name = "dashboard_detail/4_disk.html"
    app_version = APP_VERSION


class NetInterfaceView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = NetInterface
    template_name = "dashboard_detail/5_net.html"
    app_version = APP_VERSION
