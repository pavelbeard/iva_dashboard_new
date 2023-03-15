import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from http import HTTPStatus
from pprint import pprint

import requests


class PromQueryMixin:
    data_handler_class = None
    _prom_target_address = None

    def _get_promql_data(self, query):
        try:
            url = f"http://{self._prom_target_address}/api/v1/{query['query']}"
            response = requests.get(url)
            handler = self.data_handler_class(response.json())
            return {"value": handler.get_handled_data()}
        except requests.RequestException:
            return HTTPStatus.SERVICE_UNAVAILABLE

    def get_context_data(self, request, prom_target_address):
        self._prom_target_address = prom_target_address

        querylist = json.loads(request.GET['querylist'])

        with ThreadPoolExecutor(max_workers=6) as pool:
            context = [r for r in pool.map(self._get_promql_data, [q for q in querylist])]
            return context
