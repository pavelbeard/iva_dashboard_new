import json
from typing import Callable

import aiohttp.client_exceptions
from django.views import generic
from django.conf import settings
from django import http
from . import models
from .logic import IvaMetrics


class ServerInfoMixin(generic.ListView):
    cmd: str = None
    cb_handler: Callable = None
    server_config_file = settings.SERVER_CONFIG_FILE

    async def get(self, request, *args, **kwargs):
        query = models.Target.objects.all()
        targets = [
            {
                "address": q.address,
                "port": q.port,
                "username": q.username,
                "password": q.password,
                "cmd": self.cmd
            } async for q in query
        ]

        scraper = IvaMetrics(targets={"hosts": targets}, server_config_path=self.server_config_file)
        try:
            data = await scraper.scrape_metrics_from_agent()
            response_data = [self.cb_handler(d) for d in data]
            return http.JsonResponse(json.dumps(response_data), safe=False)
        except aiohttp.client_exceptions.ClientConnectionError:
            return http.JsonResponse(json.dumps({"ClientConnectionError": f"{scraper.monitor_url} is unreachable."}), safe=False)




