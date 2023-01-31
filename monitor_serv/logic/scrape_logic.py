import json
import re
import aiohttp
import yaml
from aiohttp import web
from dashboard import models


# TODO: убрать хостнеймы и создать обработчик

class ValidationException(Exception):
    def __init__(self, message):
        self.message = message


class DigitalDataConverters:
    @staticmethod
    def convert_metric_to_bytes(amount: str) -> float:
        """
        Конвертирует единицы измерения информации в метрической системе в байты.\n
        :param amount: Количество тера-, гига-, мега-, кило- и просто байтов
        :return: float
        """
        if amount.__contains__("T"):
            return float(amount[:-1]) * 1000 ** 4
        if amount.__contains__("G"):
            return float(amount[:-1]) * 1000 ** 3
        elif amount.__contains__("M"):
            return float(amount[:-1]) * 1000 ** 2
        elif amount.__contains__("K"):
            return float(amount[:-1]) * 1000
        else:
            return float(amount[:-1])

    @staticmethod
    def convert_bytes_to_metric(amount: str) -> str:
        """
        Конвертирует байты в международные единицы измерения информации в метрической системе.\n
        :param amount: Количество байтов
        :return: str
        """
        try:
            amount_of_bytes = float(amount)
            if 0.0 <= amount_of_bytes < 1000.0:
                return f"{amount_of_bytes:10.2f}B".strip()
            elif 1000.0 <= amount_of_bytes < 1_000_000.0:
                return f"{amount_of_bytes / 1000:10.2f}KB".strip()
            elif 1_000_000.0 <= amount_of_bytes < 1_000_000_000.0:
                return f"{amount_of_bytes / 1000 ** 2:10.2f}MB".strip()
            else:
                return f"{amount_of_bytes / 1000 ** 3:10.2f}GB".strip()
        except ValueError:
            return ''

    @staticmethod
    def from_cidr_to_prefixlen(ipaddr: str, netmask: str) -> str:
        splitted_nm = [
            int(i) for i in "".join(["{0:b}".format(int(octet)) for octet in netmask.split(".")]).replace("0", "")
        ]
        prefixlen = sum(splitted_nm)
        return f"{ipaddr}/{prefixlen}"


class IvaMetrics:
    def __init__(self, targets: dict, server_config_path):
        self.targets = targets
        self.server_config_path = server_config_path

        try:
            with open(self.server_config_path, 'r') as file:
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
                    if response.status == 422:
                        raise ValidationException("bad validation.")

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
                except ValidationException:
                    raise ValidationException


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

        other_data = data.split("\n")

        processes_list = []
        if other_data[0] == "no connection with server." or other_data[0] == "bad credentials.":
            return {"hostname": "hostname", "task": cls.exec_analysis.__name__, "data": [{"connection_error": True}]}

        for d in other_data[:-1]:
            *status, service = d.split()
            status = str().join(status)

            if status == "[-]":
                processes_list.append({"service": service, "status": "stopped"})
            elif status == "[+]":
                processes_list.append({"service": service, "status": "running"})
            if status == "[?]":
                processes_list.append({"service": service, "status": "not determined"})

        return {"hostname": "hostname", "task": cls.exec_analysis.__name__, "data": processes_list}

    @classmethod
    def _cpu_analysis(cls, cpu_data, core_num: int = None):
        idle = cpu_data.get('id').strip()
        total = sum(map(lambda i: float(i), (v for v in cpu_data.values())))

        key = "cpu_load" if core_num is None else f"core{core_num}"

        if total != 0:
            cpu_data |= {key: f"{(1 - float(idle) / total) * 100:10.2f}".strip()}
        else:
            cpu_data |= {key: f"{(1 - float(idle)) * 100:10.2f}".strip()}

    @classmethod
    def cpu_top_analysis(cls, data: str):
        """
        Выводит информацию о загрузке процессора, количестве ядер и загрузку каждого ядра.\n
        :param data: Данные о загрузке процессора
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.cpu_top_analysis.__name__)

        all_cores, *each_core = data.split("\n")

        if 'no connection with server.' in all_cores:
            return {"hostname": "hostname", "task": cls.cpu_top_analysis.__name__, "data": [{"connection_error": True}]}

        all_cores_data = {i[-2:]: i[:-2] for i in re.split(",\s+|,", all_cores.split(":")[1].strip()[:-1])}
        each_core_data = [{i[-2:]: i[:-2] for i in re.split(",\s+|,", x.split(":")[1].strip())} for x in each_core[:-1]]

        cls._cpu_analysis(cpu_data=all_cores_data)

        for num, core in enumerate(each_core_data):
            cls._cpu_analysis(cpu_data=core, core_num=num)

        tmp_data = [{"all_cores": all_cores_data}, {"each_core": each_core_data}]

        return {"hostname": "hostname", "task": cls.cpu_top_analysis.__name__, "data": tmp_data}

    @classmethod
    def ram_analysis(cls, data: str) -> {}:
        """
        Выводит информацию о загрузке RAM, всего RAM и свободной RAM на текущий момент
        :param data: RAM data
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.ram_analysis.__name__)

        ram_data = data.split("\n")

        if "no connection with server." in ram_data:
            return {"hostname": "hostname", "task": cls.ram_analysis.__name__, "data": [{"connection_error": True}]}

        # total used free shared buff/cache available
        ram_data = list(map(lambda x: re.split("\s+", x)[1:], ram_data[1:-1]))

        # mem
        ram_total = ram_data[0][0]
        ram_used = ram_data[0][1]
        ram_free = ram_data[0][2]
        ram_shared = ram_data[0][3]
        ram_buff_cache = ram_data[0][4]
        ram_avail = ram_data[0][5]
        ram_util = \
            f"{100 - (((float(ram_free[:-1]) + float(ram_buff_cache[:-1])) * 100) / float(ram_total[:-1])):10.2f}" \
            .strip()

        tmp_data = [
            {"ram_util": ram_util},
            {"ram_total": ram_total},
            {"ram_free": ram_free},
            {"ram_used": ram_used},
        ]

        return {"hostname": "hostname", "task": cls.ram_analysis.__name__, "data": tmp_data}

    @classmethod
    def file_sys_analysis(cls, data: str) -> {}:
        """
        Анализ данных файловой системы с сервера.\n
        :param data: Disk data
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.file_sys_analysis.__name__)

        fs_data = data.split("\n")

        tmp_data = []

        if "no connection with server." in fs_data:
            return {
                "hostname": "hostname",
                "task": cls.file_sys_analysis.__name__,
                "data": [{"connection_error": True}]
            }

        # filesystem size used available use% mounted on
        for fs in fs_data[1:-2]:
            tmp_tuple = tuple(map(lambda x: x.strip(), fs.split()))
            filesystem, size, used, available, use_percent, mounted_on = tmp_tuple
            tmp_data.append({"filesystem": filesystem, "size": size,
                             "used": used, "available": available, "use_percent": use_percent,
                             "mounted_on": mounted_on})

        most_valuable_partition = max(tmp_data,
                                      key=lambda x: DigitalDataConverters.convert_metric_to_bytes(x.get('size')))

        tmp_data += [
            {"total_disk_size": fs_data[-2].split()[3]},
            {"most_valuable_part_fs": most_valuable_partition.get('filesystem')},
            {"most_valuable_part_size": most_valuable_partition.get('size')},
            {"most_valuable_part_used": most_valuable_partition.get('used')},
            {"most_valuable_part_available": most_valuable_partition.get('available')},
            {"most_valuable_part_use_percent": most_valuable_partition.get('use_percent')},
        ]

        return {"hostname": "hostname", "task": cls.ram_analysis.__name__, "data": tmp_data}

    @classmethod
    def net_analysis(cls, data: str) -> {}:
        """
        Анализ утилизации сетевых интерфейсов командой ifconfig.\n
        :param data: Данные команды ifconfig
        :return: {}
        """
        if type(data) == dict:
            return cls.error_result(cls.net_analysis.__name__)

        net_data = data.split("\n")

        if "no connection with server." in net_data:
            return {"hostname": "hostname", "task": cls.net_analysis.__name__, "data": [{"connection_error": True}]}
        if net_data == ['']:
            return {"hostname": "hostname", "task": cls.net_analysis.__name__, "data": [
                {"command_not_found": True}
            ]}

        text = "\n".join(net_data)

        PATTERN = "(.*|.*:.*):\s.*<(\w{2,4}).*\n\s+inet\s(\d+.\d+.\d+.\d+)\s+netmask\s(\d+.\d+.\d+.\d+).*\n|" + \
                  ".*\n\s+RX\spackets\s(\d+)\s+bytes\s(\d+).*\n" + \
                  ".*RX\serrors\s(\d+)\s+dropped\s(\d+)\s+overruns\s(\d+)\s+frame\s(\d+)\n" + \
                  "\s+TX\spackets\s(\d+)\s+bytes\s(\d+)\s.*\n" + \
                  "\s+TX\serrors\s(\d+)\s+dropped\s(\d+)\s+overruns\s(\d+)\s+carrier\s(\d+)\s+collisions\s(\d+)"

        IFACES_INFO = re.findall(PATTERN, text, flags=re.MULTILINE)

        FORMAT_IFACES_INFO = []

        for i, interface in enumerate(IFACES_INFO):
            if all([x == "" for x in interface[0:3]]):
                new_array = tuple([x for x in IFACES_INFO[i - 1] + IFACES_INFO[i] if x != ""])
                FORMAT_IFACES_INFO.pop()
                FORMAT_IFACES_INFO.append(new_array)
            else:
                FORMAT_IFACES_INFO.append(interface)

        tmp_data = []

        for interface in FORMAT_IFACES_INFO:
            iface, status, ip_addr, netmask, \
                rx_bytes, rx_packets, rx_errors1, rx_errors2, rx_errors3, rx_errors4, \
                tx_bytes, tx_packets, tx_errors1, tx_errors2, tx_errors3, tx_errors4, tx_errors5 = interface
            tmp_data.append({
                "iface": iface, "status": status, "ipaddress": DigitalDataConverters.from_cidr_to_prefixlen(
                    ip_addr, netmask
                ),
                "rx_bytes": DigitalDataConverters.convert_bytes_to_metric(rx_bytes), "rx_packets": rx_packets,
                "rx_errors": {
                    "errors": rx_errors1, "dropped": rx_errors2, "overruns": rx_errors3, "frame": rx_errors4,
                },
                "tx_bytes": DigitalDataConverters.convert_bytes_to_metric(tx_bytes), "tx_packets": tx_packets,
                "tx_errors": {
                    "errors": tx_errors1, "dropped": tx_errors2, "overruns": tx_errors3,
                    "carrier": tx_errors4, "collisions": tx_errors5,
                },
            })

        return {"hostname": "hostname", "task": cls.net_analysis.__name__, "data": tmp_data}

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

    @classmethod
    def hostnamectl(cls, data: str) -> {}:
        """
        Основные данные сервера: hostname, os_version, os_kernel
        :return: {}
        """

        if type(data) == dict:
            return cls.error_result(cls.uptime.__name__)

        splitted_data = data.split("\n")

        hostname = splitted_data[0]
        os_version = re.search("PRETTY_NAME=\"(.*)\"", data)[1]
        os_kernel = splitted_data[1]

        return {
            "task": cls.hostnamectl.__name__,
            "data": [{"hostname": hostname, "os": os_version, "kernel": os_kernel}]
        }


class DataAccessLayerServer:
    @classmethod
    async def check_server_data(cls, data: dict):
        # query = models.Server(**data)

        # exist_server: models.Server = await models.Server.objects.aget(target_uuid=query.target_uuid)

        #
        # if len(exist_server) > 0:
        #     pass

        # exist_server = await sync_to_async(models.Server.objects.get)(target_uuid=query.target_uuid)

        # print(query)
        # await sync_to_async(query.save)()
        #
        # return {"status": "ok"}
        pass

    # SERVER CRUD
    # Create
    @classmethod
    def __insert_into_server(cls, query: models.Target):
        print(query)
        query.save()

        pass
