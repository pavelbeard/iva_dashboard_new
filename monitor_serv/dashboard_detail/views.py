from django.views.generic import TemplateView

from core_logic.chart import Chart, DiskSpaceChart, NetInterfaceChart
from core_logic.views import (
    AppVersionMixin,
    ContextDataFromImporterMixin,
    DatetimeFiltersMixin,
)
from core_logic.filters import BaseDatetimeFilter, filters_dict
from dashboard.models import CPU, RAM, DiskSpace, NetInterface, LoadAverage


# Create your views.py here.

class CPUDetailView(
    AppVersionMixin,
    ContextDataFromImporterMixin,
    DatetimeFiltersMixin,
    TemplateView,
):
    model = CPU
    template_name = "dashboard_detail/parts/1_cpu.html"
    reverse_style_url = "dashboard_detail:cpu"
    chart_class = Chart
    keys = ((
        "cpu_idle", "cpu_iowait", "cpu_irq",
        "cpu_nice", "cpu_softirq", "cpu_steal",
        "cpu_sys", "cpu_user"
    ), )
    filter = filters_dict.get_filter("from1hour")


class RAMDetailView(
    AppVersionMixin,
    ContextDataFromImporterMixin,
    DatetimeFiltersMixin,
    TemplateView,
):
    model = RAM
    template_name = "dashboard_detail/parts/2_ram.html"
    reverse_style_url = "dashboard_detail:ram"
    chart_class = Chart
    keys = (
        ("total_ram", ),
        ("ram_used", "ram_free", "ram_shared",
         "ram_buff_cache", "ram_avail")
    )


class DiskSpaceDetailView(
    AppVersionMixin,
    ContextDataFromImporterMixin,
    DatetimeFiltersMixin,
    TemplateView
):
    model = DiskSpace
    template_name = "dashboard_detail/parts/3_disk.html"
    reverse_style_url = "dashboard_detail:disk"
    chart_class = DiskSpaceChart
    keys = (
        ("fs_size", ),
        ("fs_used", ),
        ("fs_avail", ),
    )


class NetInterfaceView(
    AppVersionMixin,
    ContextDataFromImporterMixin,
    DatetimeFiltersMixin,
    TemplateView
):
    model = NetInterface
    template_name = "dashboard_detail/parts/4_net.html"
    reverse_style_url = "dashboard_detail:net"
    chart_class = NetInterfaceChart
    keys = (
        ("rx_bytes", "tx_bytes"),
        ("rx_packets", "tx_packets"),
        ("rx_errors_errors", "rx_errors_dropped"),
    )


class LoadAverageView(AppVersionMixin, ContextDataFromImporterMixin, DatetimeFiltersMixin, TemplateView):
    model = LoadAverage
    template_name = "dashboard_detail/parts/5_load_average.html"
    reverse_style_url = "dashboard_detail:load_average"
    chart_class = Chart
    keys = (
        ("one_min", "five_min", "fteen_min"),
    )
