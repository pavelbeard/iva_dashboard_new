import json

from django import http
from django.conf import settings
from django.views import generic
from monitor_srv.monitor_server.servers.logic import IvaMetrics, IvaMetricsHandler
from .mixins import ServerInfoMixin

# Create your views here.


class ServersMetricsLogicView(generic.ListView):
    server_config_file = settings.SERVER_CONFIG_FILE
    known_hosts_path = settings.KNOWN_HOSTS_FILE

    async def get(self, request, *args, **kwargs):
        scraper = IvaMetrics(server_config_path=self.server_config_file,
                             known_hosts_path=self.known_hosts_path)
        data_handler = IvaMetricsHandler()

        commands = [
            "uname -n && service --status-all",
            "uname -n && service --status-all",

        ]

        scraped_data = await scraper.get_metrics_from_target_hosts('uname -n && service --status-all')

        # TODO: настроить отображение данных

        # data_handler.service_status_all()

        response = []
        for data in scraped_data:
            if isinstance(data, Exception):
                response.append({"err_message": data.args[0]})
            elif isinstance(data[1], dict):
                response.append(data[1].get('message'))
            else:
                response.append(data_handler.service_status_all(data))

        return http.JsonResponse(json.dumps(response), safe=False)


class ServerProcesses(ServerInfoMixin):
    cmd = "uname -n && service --status-all"
    cb_handler = IvaMetricsHandler.service_status_all
