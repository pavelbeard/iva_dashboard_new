import json
import re
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
    def error_result(cls, task: str) -> dict:
        """
        Обработчик непредвиденных ошибок в данных, пришедших с сервера.\n
        :param task: Имя задачи, в которой возникла ошибка
        :return: dict[NO DATA]
        """
        return {"hostname": "no_data", "task": task, "data": [{"no_data": "no_data"}]}

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
    def exec_analysis(cls, data: str) -> {}:
        """
        Парсит команду service --status-all.\n
        :param data: Данные, выведенные командой
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.exec_analysis.__name__)

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

        return {"hostname": hostname, "task": cls.exec_analysis.__name__, "data": processes_list}

    @classmethod
    def cpu_analysis(cls, data: str) -> {}:
        """
        Выводит информацию о загрузке процессора, количестве ядер и загрузку каждого ядра.\n
        :param data: Данные о загрузке процессора
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.cpu_analysis.__name__)

        hostname, all_cores, *remaining_cores = data.split("\n")

        # промежуточный контейнер данных
        tmp_data = []

        try:
            # cpu load - all cores
            # user + nice + system + idle + iowait + irq + sortirq
            idle, total = all_cores.split()[1:][3], sum(map(lambda x: int(x), all_cores.split()[1:]))
            cpu_load = (1.0 - float(idle) / total) * 100.0

            tmp_data += [
                {"cpu_load": f"{cpu_load:10.2f}".strip()},
                {"cpu_idle": f"{100 - cpu_load:10.2f}".strip()},
            ]

            # cpu load even core
            for num, core in enumerate(list(filter(lambda x: re.search('^cpu', x), remaining_cores))):
                idle, total = core.split()[1:][3], sum(map(lambda x: int(x), core.split()[1:]))
                core_load = (1.0 - float(idle) / total) * 100.0

                tmp_data.append({f"cpu_core{num}": f"{core_load:10.2f}".strip()})
            else:
                tmp_data.append({"cpu_cores": len(tmp_data[2:])})

        except IndexError:
            tmp_data = ["no connection with server."]

        return {"hostname": hostname, "task": cls.cpu_analysis.__name__, "data": tmp_data}

    @classmethod
    def ram_analysis(cls, data: str) -> {}:
        """
        Выводит информацию о загрузке RAM, всего RAM и свободной RAM на текущий момент
        :param data: RAM data
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.ram_analysis.__name__)

        hostname, *ram_data = data.split("\n")

        # total used free shared buff/cache available
        ram_calc_data = list(map(lambda x: int(x), ram_data[1].split()[1:]))
        ram_utilization = f"{float((ram_calc_data[0] - ram_calc_data[-1]) / ram_calc_data[0] * 100):10.2f}"
        ram_total = f"{float(ram_calc_data[0] / (1000 ** 2)):10.2f}"
        ram_free = f"{float(ram_calc_data[2] / (1000 ** 2)):10.2f}"
        ram_used = f"{float((ram_calc_data[1] + ram_calc_data[3] + ram_calc_data[4]) / (1000 ** 2)):10.2f}"

        tmp_data = [
            {"ram_util": ram_utilization},
            {"ram_total": ram_total},
            {"ram_free": ram_free},
            {"ram_used": ram_used},
        ]

        return {"hostname": hostname, "task": cls.ram_analysis.__name__, "data": tmp_data}

    @classmethod
    def file_sys_analysis(cls, data: str) -> {}:
        """
        Анализ данных файловой системы с сервера.\n
        :param data: Disk data
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.file_sys_analysis.__name__)

        hostname, *fs_data = data.split("\n")

        tmp_data = []
        total = []
        total_used = []
        total_available = []

        # filesystem size used available use% mounted on
        for fs in fs_data[1:-1]:
            tmp_tuple = tuple(map(lambda x: x.strip(), fs.split()))
            filesystem, size, used, available, use_percent, mounted_on = tmp_tuple
            tmp_data.append({"filesystem": filesystem, "size": size,
                             "used": total_used, "available": available, "use_percent": use_percent,
                             "mounted_on": mounted_on})

            total.append(float(size[:-1]) if len(size) > 1 else size)
            total_used.append(float(used[:-1]) if len(used) > 1 else used)
            total_available.append(float(available[:-1]) if len(available) > 1 else available)
            total_available.append(int(use_percent[:-1]))


        return {"hostname": hostname, "task": cls.ram_analysis.__name__, "data": tmp_data}