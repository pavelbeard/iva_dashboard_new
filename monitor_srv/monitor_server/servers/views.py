import json

import aiohttp
import yaml
from django import http
from django.shortcuts import render
from django.views import generic
from django.conf import settings

from monitor_srv.monitor_server.servers.logic import IvaMetrics


# Create your views here.


# class ServersMetricsLogicView(ServerMixin):
#     monitor_url = "http://localhost:8000/api/monitor/metrics"


class ServersMetricsLogicView(generic.ListView):
    server_config_file = settings.SERVER_CONFIG_FILE
    known_hosts_path = settings.KNOWN_HOSTS_FILE

    async def get(self, request, *args, **kwargs):
        scraper = IvaMetrics(server_config_path=self.server_config_file,
                             known_hosts_path=self.known_hosts_path)

        commands = [
            "uname -n && service --status-all",
            "uname -n && service --status-all",

        ]

        scraped_data = await scraper.get_metrics_from_target_hosts('uname -n && service --status-all')

        response = []
        for data in scraped_data:
            if isinstance(data, Exception):
                response.append({"err_message": data.args[0]})
            else:
                response.append(data[1].split("\n"))

            # async with aiohttp.ClientSession() as session:
            #     async with session.post(url=scraper_url, data=)

        return http.JsonResponse(json.dumps(response), safe=False)


def server_metrics_view(request):
    return None
