from core_logic.views import AppVersionMixin, ContextDataFromImporterMixin, DatetimeFiltersMixin
from dashboard.models import CPU, RAM, DiskSpace, NetInterface, LoadAverage
from django.views.generic import TemplateView

from monitor_serv import settings


# Create your views.py here.

class CPUDetailView(AppVersionMixin, ContextDataFromImporterMixin, DatetimeFiltersMixin, TemplateView):
    model = CPU
    template_name = "dashboard_detail/parts/1_cpu.html"
    reverse_style_url = "dashboard_detail:cpu"


class RAMDetailView(AppVersionMixin, ContextDataFromImporterMixin, DatetimeFiltersMixin, TemplateView):
    model = RAM
    template_name = "dashboard_detail/parts/2_ram.html"
    reverse_style_url = "dashboard_detail:ram"


class DiskSpaceDetailView(AppVersionMixin, ContextDataFromImporterMixin, DatetimeFiltersMixin, TemplateView):
    model = DiskSpace
    template_name = "dashboard_detail/parts/3_disk.html"
    reverse_style_url = "dashboard_detail:disk"


class NetInterfaceView(AppVersionMixin, ContextDataFromImporterMixin, DatetimeFiltersMixin, TemplateView):
    model = NetInterface
    template_name = "dashboard_detail/parts/4_net.html"
    reverse_style_url = "dashboard_detail:net"


class LoadAverageView(AppVersionMixin, ContextDataFromImporterMixin, DatetimeFiltersMixin, TemplateView):
    model = LoadAverage
    template_name = "dashboard_detail/parts/4_net.html"
    reverse_style_url = "dashboard_detail:load_average"
