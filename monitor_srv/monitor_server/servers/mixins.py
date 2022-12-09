import asyncio
import json

import aiohttp
import iva_dashboard as asyncssh
import requests
from django import views
from django.shortcuts import render
from django.views import generic
from django.conf import settings

from monitor_srv.monitor_server.monitor_server.decorators import timed_lru_cache


class ServerMixin(generic.ListView):
    model = None
    context_object_name = None
    template_name = None
    hosts: dict = settings.MONITORING_TARGETS
    known_hosts = settings.KNOWN_HOSTS_FILE
    monitor_url: str = None
    targets: set = None

    async def scrape_data(self, founded_host: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.monitor_url, headers={"Content-Type": "application/json"},
                data=json.dumps(founded_host)
            ) as resp:
                json_content = await resp.json()
                return resp.status, json_content

    @timed_lru_cache(seconds=3600)
    def get_keys_from_known_hosts_file(self):
        with open(self.known_hosts) as file:
            rows = "\n".join(list(filter(lambda r: r != "", file.read().split("\n"))))

            return rows

    async def get_monitoring_data(self):
        founded_host = [host for host in self.hosts if self.targets.intersection(set(host.values()))][0]

        keys = self.get_keys_from_known_hosts_file()
        founded_host.update({"keys": keys})
        task = asyncio.create_task(self.scrape_data(founded_host))

        return await task

    async def get(self, request, *args, **kwargs):
        data = await self.get_monitoring_data()

        status_code, data = data

        if status_code == 408:
            return render(request, self.template_name, context={
                "message": data.get('message')
            }, status=status_code)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "hostname": data.get("hostname"),
                "data": data.get("data")
            }
        )
