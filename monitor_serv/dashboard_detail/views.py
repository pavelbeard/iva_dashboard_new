from core_logic.views import AppVersionMixin, ContextDataFromImporterMixin
from dashboard.models import CPU, RAM, DiskSpace, NetInterface
from django.views.generic import TemplateView

from monitor_serv import settings


# Create your views.py here.

class CPUDetailView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = CPU
    template_name = "dashboard_detail/parts/1_cpu.html"


class RAMDetailView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = RAM
    template_name = "dashboard_detail/parts/2_ram.html"


class DiskSpaceDetailView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = DiskSpace
    template_name = "dashboard_detail/parts/3_disk.html"


class NetInterfaceView(AppVersionMixin, ContextDataFromImporterMixin, TemplateView):
    model = NetInterface
    template_name = "dashboard_detail/parts/4_net.html"
