import aiohttp
import json
from typing import Callable
from django import http
from django.conf import settings
from django.views import generic
from django.db import utils
from logic import IvaMetrics, TargetsIsEmpty, ValidationException
from . import models


class ServerAnalysisMixin(generic.ListView):
    cmd: str = None
    callback_iva_metrics_handler: Callable = None
    server_config_file = settings.SERVER_CONFIG_FILE

    async def get(self, request, *args, **kwargs):
        scraper = None
        try:
            query = models.Target.objects.all()
            targets = [
                {
                    "host": q.address,
                    "port": q.port,
                    "username": q.username,
                    "password": q.password,
                    "cmd": self.cmd
                } async for q in query
            ]

            if len(targets) == 0:
                raise TargetsIsEmpty(message="The table 'Targets' is empty!")

            scraper = IvaMetrics(targets={"hosts": targets}, server_config_path=self.server_config_file)
            data = await scraper.scrape_metrics_from_agent()

            # TODO: добавить экспорт метрик в базу данных

            response_data = [self.callback_iva_metrics_handler(d) for d in data]

            for rd, target in zip(response_data, targets):
                if rd is not None:
                    rd['id'] = f"{target.get('host')}:{target.get('port')}"

            return http.JsonResponse(json.dumps(response_data), safe=False)
        except aiohttp.ClientConnectionError:
            return http.JsonResponse(json.dumps({"ClientConnectionError": f"{scraper.monitor_url} is unreachable."}),
                                     safe=False)
        except utils.ProgrammingError:
            return http.JsonResponse(json.dumps({"ProgrammingError": "The table 'Targets' is not exists!"}),
                                     safe=False)
        except FileNotFoundError:
            return http.JsonResponse(json.dumps({"FileNotFoundError": "Config file not found."}),
                                     safe=False)
        except TargetsIsEmpty as tie:
            return http.JsonResponse(json.dumps({"TargetsIsEmpty": tie.message}), safe=False)
        except ValidationException as err:
            return http.JsonResponse(json.dumps({"ValidationException": err.message}), safe=False)

