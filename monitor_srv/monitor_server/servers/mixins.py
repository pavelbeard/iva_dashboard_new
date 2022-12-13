import json
from typing import Callable
from django.conf import settings
from django.views import generic
from django import http
from .logic import IvaMetrics, IvaMetricsHandler


class ServerInfoMixin(generic.ListView):
    server_config_file = settings.SERVER_CONFIG_FILE
    known_hosts_path = settings.KNOWN_HOSTS_FILE
    cmd: str = None
    cb_handler: Callable = None

    async def get(self, request, *args, **kwargs):
        scraper = IvaMetrics(
            server_config_path=self.server_config_file,
            known_hosts_path=self.known_hosts_path
        )

        scraped_data = await scraper.get_metrics_from_target_hosts(self.cmd)

        response_body = []
        for data in scraped_data:
            if isinstance(data, Exception):
                response_body.append({"err_message": data.args[0]})
            elif isinstance(data[1], dict):
                response_body.append(data[1].get('message'))
            else:
                response_body.append(self.cb_handler(data))

        return http.JsonResponse(json.dumps(response_body), safe=False)
