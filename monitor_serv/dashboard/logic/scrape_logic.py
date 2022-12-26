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
            return {"hostname": hostname, "task": cls.exec_analysis.__name__, "data": [{"connection_error": True}]}
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

        if 'no connection with server.' in all_cores:
            return {"hostname": hostname, "task": cls.cpu_analysis.__name__, "data": [{"connection_error": True}]}

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
            tmp_data = [{"connection_error": True}]

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

        if "no connection with server." in ram_data:
            return {"hostname": hostname, "task": cls.ram_analysis.__name__, "data": [{"connection_error": True}]}

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

        if "no connection with server." in fs_data:
            return {"hostname": hostname, "task": cls.file_sys_analysis.__name__, "data": [{"connection_error": True}]}

        # filesystem size used available use% mounted on
        for fs in fs_data[1:-2]:
            tmp_tuple = tuple(map(lambda x: x.strip(), fs.split()))
            filesystem, size, used, available, use_percent, mounted_on = tmp_tuple
            tmp_data.append({"filesystem": filesystem, "size": size,
                             "used": used, "available": available, "use_percent": use_percent,
                             "mounted_on": mounted_on})

        most_valuable_partition = max(tmp_data, key=lambda x: float(x.get('size')[:-1]))

        tmp_data += [
            {"total_disk_size": fs_data[-2].split()[3]},
            {"most_valuable_part_fs": most_valuable_partition.get('filesystem')},
            {"most_valuable_part_size": most_valuable_partition.get('size')},
            {"most_valuable_part_used": most_valuable_partition.get('used')},
            {"most_valuable_part_available": most_valuable_partition.get('available')},
            {"most_valuable_part_use_percent": most_valuable_partition.get('use_percent')},
        ]

        return {"hostname": hostname, "task": cls.ram_analysis.__name__, "data": tmp_data}

    @classmethod
    def net_analysis(cls, data: str) -> {}:
        """
        Анализ данных сетевых интерфейсов с сервера.\n
        :param data: Net data
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.net_analysis.__name__)

        hostname, *net_data = data.split("\n")

        if "no connection with server." in net_data:
            return {"hostname": hostname, "task": cls.net_analysis.__name__, "data": [{"connection_error": True}]}
        if net_data == ['']:
            return {"hostname": hostname, "task": cls.net_analysis.__name__, "data": [{"command_not_found": True}]}

        text = "\n".join(net_data)

        INTERFACE = re.search(r"on\s(.*)", text)
        PATTERN = "\s+(\db|\d+b|\d+.\d+b|\dKb|\d+Kb|\d+.\d+Kb|\dMb|\d+Mb|\d+.\d+Mb|\dGb|\d+Gb|\d+.\d+Gb|" + \
                  "\dB|\d+B|\d+.\d+B|\dKB|\d+KB|\d+.\d+KB|\dMB|\d+MB|\d+.\d+MB|\dGB|\d+GB|\d+.\d+GB)"
        TOTAL_SEND_RATE = re.search(fr"Total\ssend\srate:{PATTERN}{PATTERN}{PATTERN}", text)
        TOTAL_RECEIVE_RATE = re.search(fr"Total\sreceive\srate:{PATTERN}{PATTERN}{PATTERN}", text)
        TOTAL_SEND_AND_RECEIVE_RATE = re.search(fr"Total\ssend\sand\sreceive\srate:{PATTERN}{PATTERN}{PATTERN}", text)
        PEAK_RATE = re.search(fr"Peak\srate\s\(.*\):\s+{PATTERN}{PATTERN}{PATTERN}", text)
        CUMULATIVE = re.search(fr"Cumulative\s\(.*\):\s+{PATTERN}{PATTERN}{PATTERN}", text)
        FROM_TO = re.findall(fr"(.*):\d+\s+(<=|=>){PATTERN}{PATTERN}{PATTERN}{PATTERN}", text)

        tmp_data = [
            {"interface": INTERFACE[1]}
        ]

        try:
            for match in FROM_TO:
                direction = "from" if "=>" in match[1] else "to"
                tmp_data.append({
                    direction: match[0].strip() + match[1],
                    "last2s": match[2],
                    "last10s": match[3],
                    "last40s": match[4],
                    "cumulative": match[5]
                })
        except TypeError:
            pass

        tmp_data += [
            {
                "total_send_rate": {
                    "last2s": TOTAL_SEND_RATE[1], "last10s": TOTAL_SEND_RATE[2], "last40s": TOTAL_SEND_RATE[3]
                }
            },
            {
                "total_receive_rate": {
                    "last2s": TOTAL_RECEIVE_RATE[1], "last10s": TOTAL_RECEIVE_RATE[2], "last40s": TOTAL_RECEIVE_RATE[3]
                }
            },
            {
                "total_send_and_receive_rate": {
                    "last2s": TOTAL_SEND_AND_RECEIVE_RATE[1],
                    "last10s": TOTAL_SEND_AND_RECEIVE_RATE[2],
                    "last40s": TOTAL_SEND_AND_RECEIVE_RATE[3]
                }
            },
            {"peak_rate": {"last2s": PEAK_RATE[1], "last10s": PEAK_RATE[2], "last40s": PEAK_RATE[3]}},
            {"cumulative": {"last2s": CUMULATIVE[1], "last10s": CUMULATIVE[2], "last40s": CUMULATIVE[3]}},
        ]

        if "no connection with server." in net_data:
            return {"hostname": hostname, "task": cls.net_analysis.__name__, "data": [{"connection_error": True}]}

        return {"hostname": hostname, "task": cls.net_analysis.__name__, "data": tmp_data}

    @classmethod
    def uptime(cls, data: str) -> {}:
        """
        Показывает, сколько времени сервер находится в работе
        :param data: uptime
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.uptime.__name__)

        hostname, *uptime_data = data.split("\n")

        if "no connection with server." in uptime_data:
            return {"hostname": hostname, "task": cls.uptime.__name__, "data": [{"connection_error": True}]}

        tmp_data = [{"uptime": uptime_data[0].split(',')[0]}]

        return {"hostname": hostname, "task": cls.uptime.__name__, "data": tmp_data}
