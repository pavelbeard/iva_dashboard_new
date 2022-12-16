import json
import aiohttp
import yaml
from aiohttp import web


class IvaMetrics:
    def __init__(self, targets: dict, server_config_path):
        self.targets = targets
        self.server_config_path = server_config_path

        try:
            with open(self.server_config_path) as file:
                self.__config = yaml.safe_load(file)
                self.monitor_url = self.__config.get('settings').get('scraper_url')
        except FileNotFoundError:
            raise FileNotFoundError

    async def scrape_metrics_from_agent(self):
        """Собирает метрики с агента"""
        headers = {"Content-Type": "application/json;charset=utf-8"}
        body = json.dumps(self.targets).encode('utf-8')
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.monitor_url, headers=headers, data=body) as response:
                try:
                    json_content = await response.json()
                    return json_content
                except aiohttp.ClientConnectionError:
                    raise aiohttp.ClientConnectionError
                except web.HTTPNotFound:
                    raise web.HTTPNotFound
                except aiohttp.ContentTypeError:
                    raise aiohttp.ContentTypeError
                except aiohttp.ClientResponseError:
                    raise aiohttp.ClientResponseError


class IvaMetricsHandler:
    @classmethod
    def systemctl_list_units_parser(cls, data: str) -> {}:
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

        return {"hostname": hostname, "task": cls.systemctl_list_units_parser.__name__, "data": tmp_list}

    @classmethod
    def service_status_all(cls, data: str) -> {}:
        """
        Парсит команду service --status-all.\n
        :param data: Данные, выведенные командой
        :return: {}
        """
        if type(data) == dict:
            return {"hostname": "no_data", "task": cls.service_status_all.__name__,
                    "data": [{"no_data": "no_data"}]}

        hostname, *other_data = data.split("\n")

        processes_list = []
        if other_data[0] == "no connection with server." or other_data[0] == "bad credentials.":
            processes_list.append(other_data[0])
        else:
            for d in other_data[:-1]:
                *status, service = d.split()
                status = str().join(status)

                if status == "[-]":
                    processes_list.append({"service": service, "status": "stopped"})
                elif status == "[+]":
                    processes_list.append({"service": service, "status": "running"})
                if status == "[?]":
                    processes_list.append({"service": service, "status": "not determined"})

        return {"hostname": hostname, "task": cls.service_status_all.__name__, "data": processes_list}

    @classmethod
    def cpu_utilization(cls, data: str) -> {}:
        """
        Выводит информацию о загрузке процессора.\n
        :param data: Данные о загрузке процессора
        """
        if type(data) == dict:
            return {"hostname": "no_data", "task": cls.cpu_utilization.__name__,
                    "data": [{"no_data": "no_data"}]}

        hostname, cpu_load = data.split("\n")

        return {"hostname": hostname, "task": cls.cpu_utilization.__name__, "data": cpu_load}

