import asyncio
import json
from functools import lru_cache

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
    encryption_key = settings.ENCRYPTION_KEY

    @staticmethod
    async def get_settings():
        dboard_settings = await models.DashboardSettings.objects.aget(command_id=1)
        return {
            'scraper_url': dboard_settings.scraper_url,
            'scrape_interval': dboard_settings.scrape_interval
        }

    @staticmethod
    def _json_response(data) -> http.JsonResponse:
        return http.JsonResponse(json.dumps(data), safe=False)

    @staticmethod
    def _update_response_data(response_data: list, targets: list):
        """Вспомогательный метод для дополнения ответных данных"""
        for rd, target in zip(response_data, targets):
            if rd is not None:
                rd['pk'] = target.get('pk')
                rd['id'] = f"{target.get('host').replace('.', '')}{target.get('port')}"
                rd['role'] = f"{target.get('role')}"

    async def _scrape_data(self, targets, scraper):
        try:
            data = await scraper.scrape_metrics_from_agent()
            result = [self.callback_iva_metrics_handler(d) for d in data]
            return result
        except aiohttp.ClientConnectionError as e:
            raise aiohttp.ClientConnectionError

    @lru_cache(3)
    async def _get_targets(self) -> list:
        """Воспомогательный метод для получения целевых хостов"""
        query = self.__target.objects.filter(is_being_scan=True)
        targets = [
            {
                "pk": q.id,
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
        tasks = []
        scraper = None
        try:
            # get targets
            targets = await self._get_targets()

            # get dboard_settings
            dboard_settings = await self.get_settings()

            # scrape data
            scraper = IvaMetrics(targets={"hosts": targets}, settings=dboard_settings)
            response_data = await self._scrape_data(targets, scraper)

            # send to db
            if self.callback_data_access_layer is not None:
                tasks = [asyncio.create_task(
                    self.callback_data_access_layer(target_pk=t.get('pk'), data=el)
                ) for t, el in zip(targets, response_data)]

            # update data
            self._update_response_data(response_data, targets)

            # return!
            return self._json_response(response_data)
        except aiohttp.ClientConnectionError:
            return self._json_response({"ClientConnectionError": f"{scraper.monitor_url} is unreachable."})
        except utils.ProgrammingError:
            return self._json_response({"ProgrammingError": "The table 'Targets' is not exists!"})
        except models.DashboardSettings.DoesNotExist:
            return self._json_response({"DoesNotExist": "SettingsObject not found."})
        except TargetsIsEmpty as tie:
            return self._json_response({"TargetsIsEmpty": tie.message})
        except ValidationException as err:
            return self._json_response({"ValidationException": err.message})
        finally:
            # await a work with db
            if self.callback_data_access_layer is not None:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                print(results)
            # TODO: логировать вывод gather
