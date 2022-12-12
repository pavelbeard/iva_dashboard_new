import asyncio
import json
from typing import Any

import aiohttp
import yaml
from aiohttp import web
from .extentions import timed_lru_cache


class IvaMetrics:
    def __init__(self, server_config_path: str, known_hosts_path):
        """
        Создает класс IvaMetrics с параметрами: \n
        :param server_config_path: Путь к конфигу сервера мониторинга
        :param known_hosts_path: Путь к файлу с открытыми ключами хостов.
        Перед тем, как запускать сервер, необходимо запустить скрипт scan-keys
        """
        self.server_config_path = server_config_path
        self.known_hosts_path = known_hosts_path

        with open(self.server_config_path) as file:
            self.__config = yaml.safe_load(file)
            self.monitor_url = self.__config.get('settings').get('scraper_url')

    async def scrape_metrics_from_agent(self, target_host: dict) -> tuple[int, Any]:
        """
        Собирает метрики c агента
        :param target_host: Целевой хост из конфигурации сервера, подлежащий мониторингу
        :return: tuple[int, Any] - статус-код и данные с целевого хоста
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=self.monitor_url, headers={"Content-Type": "application/json"},
                    data=json.dumps(target_host)
            ) as resp:
                try:
                    json_content = await resp.json()
                    return resp.status, json_content
                except aiohttp.ClientConnectionError:
                    raise aiohttp.ClientConnectionError
                except web.HTTPNotFound:
                    raise web.HTTPNotFound
                except aiohttp.ContentTypeError:
                    raise aiohttp.ContentTypeError
                except aiohttp.ClientResponseError:
                    raise aiohttp.ClientResponseError

    @timed_lru_cache(seconds=3600)
    def get_public_keys_from_known_hosts_file(self):
        """
        Читает файл known_hosts и\n
        :return: возвращает открытые ключи целевых хостов
        """
        with open(self.known_hosts_path) as file:
            rows = "\n".join(list(filter(lambda r: r != "", file.read().split("\n"))))
            return rows

    async def get_metrics_from_target_hosts(self, cmd: str) -> tuple:
        """
        Собирает метрики с целевых хостов. Метрики собираются с помощью параметра\n
        :param cmd: cmd - команда мониторинга, запускающаяся на целевых хостах
        :return: tuple
        """
        target_hosts = [host for host in self.__config.get('hosts')]

        keys = self.get_public_keys_from_known_hosts_file()

        for i in range(len(target_hosts)):
            target_hosts[i].update({"keys": keys, "cmd": cmd})

        try:
            tasks = [asyncio.create_task(self.scrape_metrics_from_agent(fh)) for fh in target_hosts]
            results = await asyncio.gather(*tasks)

            return results
        except aiohttp.ClientConnectionError:
            raise aiohttp.ClientConnectionError("No connection with agent")
        except web.HTTPNotFound:
            raise web.HTTPNotFound
        except aiohttp.ContentTypeError:
            raise aiohttp.ContentTypeError
        except aiohttp.ClientResponseError:
            raise aiohttp.ClientResponseError


class IvaMetricsHandler(IvaMetrics):
    def systemctl_list_units_parser(self, data: str) -> {}:
        """
        Парсит команду systemctl list-units --type=service.\n
        :param data: Данные, выведенные командой
        :return: :{}:
        """
        hostname, *other_data = data.split("\n")

        tmp_list = []  # временный список для данных
        for row in other_data[1:-7]:
            tmp = row.split()[1:] + ['failed'] if "●" in row else row.split()
            unit, load, active, sub, *desc = tmp
            tmp_list.append({"unit": unit, "load": load, "active": active, "sub": sub})

        return {"hostname": hostname, "task": self.systemctl_list_units_parser.__name__, "data": tmp_list}

    def service_status_all(self, data: str) -> {}:
        """
        Парсит команду service --status-all.\n
        :param data: Данные, выведенные командой
        :return: {}
        """
        hostname, *other_data = data.split("\n")

        tmp_list = []
        for d in other_data[:-1]:
            *status, service = d.split()
            status = str().join(status)

            if status == "[-]":
                tmp_list.append({"service": service, "status": "stopped"})
            elif status == "[+]":
                tmp_list.append({"service": service, "status": "running"})
            if status == "[?]":
                tmp_list.append({"service": service, "status": "not determined"})

        return {"hostname": hostname, "task": self.service_status_all.__name__, "data": tmp_list}
