from django.shortcuts import render

# Create your views here.

from logic import IvaMetricsHandler
from . import mixins


def index(request):
    return render(request, template_name="dashboard_detail/index.html")


class NetDetail(mixins.ServerAnalysisDetailMixin):
    # команды iftop может не быть на целевой машине, проверить перед
    # развертыванием дашборда, установить в случае отсутствия
    # UPD: дано разрешение выполнять команду iftop без прав админа: sudo chmod +s $(which /usr/sbin/iftop)
    cmd = "uname -n && /usr/sbin/iftop -t -s 1 -P"
    callback_iva_metrics_handler = IvaMetricsHandler.net_analysis_detail
