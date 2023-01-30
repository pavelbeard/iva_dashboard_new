import asyncio
import json
import aiohttp
from typing import Callable
from django import http, shortcuts
from django.conf import settings
from django.db import utils
from django.views import generic
from logic import (
    IvaMetrics,
    TargetsIsEmpty,
    ValidationException,
    pass_handler,
)
from . import models


class ServerAnalysisMixin(generic.ListView):
    __target = models.Target

    cmd: str = None
    callback_iva_metrics_handler: Callable = None
    callback_insert_into_table: Callable = None
    callback_data_access_layer: Callable = None
    server_config_file = settings.SERVER_CONFIG_FILE
    encryption_key = settings.ENCRYPTION_KEY

    @classmethod
    def _update_response_data(cls, response_data: list, targets: list) -> {}:
        for rd, target in zip(response_data, targets):
            if rd is not None:
                rd['id'] = f"{target.get('host').replace('.', '')}{target.get('port')}"
                rd['role'] = f"{target.get('role')}"

    async def _get_targets(self):
        query = self.__target.objects.all()
        targets = [
            {
                "host": q.address,
                "port": q.port,
                "username": q.username,
                "password": pass_handler.decrypt_pass(self.encryption_key, q.password),
                "cmd": self.cmd,
                "role": q.server_role,
            } async for q in query
        ]

        if len(targets) == 0:
            raise TargetsIsEmpty(message="The table 'Targets' is empty!")

        return targets

    async def get(self, request, *args, **kwargs):
        scraper = None
        try:
            targets = await self._get_targets()
            scraper = IvaMetrics(targets={"hosts": targets}, server_config_path=self.server_config_file)
            data = await scraper.scrape_metrics_from_agent()

            response_data = [self.callback_iva_metrics_handler(d) for d in data]

            # TODO: добавить экспорт метрик в базу данных
            tasks_export_to_db = None

            self._update_response_data(response_data, targets)

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
