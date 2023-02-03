import json
import re

import aiohttp
from aiohttp import web
from asgiref.sync import sync_to_async
from django.utils import timezone

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
    def __init__(self, targets: dict, settings):
        self.targets = targets
        self.settings = settings
        self.monitor_url = self.settings.get('scraper_url')

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
        if "no connection with server." in data or "bad credentials." in data:
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

        if 'no connection with server.' in data:
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

        if "no connection with server." in data:
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

        __ram_free = DigitalDataConverters.convert_metric_to_bytes(ram_free)
        __ram_buff_cache = DigitalDataConverters.convert_metric_to_bytes(ram_buff_cache)
        __ram_total = DigitalDataConverters.convert_metric_to_bytes(ram_total)

        ram_util = f"{100 - (((__ram_free + __ram_buff_cache) * 100) / __ram_total):10.2f}".strip()

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

        if "no connection with server." in data:
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

        if "no connection with server." in data:
            return {"hostname": "hostname", "task": cls.net_analysis.__name__, "data": [
                {"connection_error": True}
            ]}
        elif data == ['']:
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

        if "no connection with server." in data:
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

        if "no connection with server." in data:
            return {"failed": "hostname", "task": cls.uptime.__name__, "data": [{"connection_error": True}]}

        hostname = splitted_data[0]
        os_version = re.search("PRETTY_NAME=\"(.*)\"", data)[1]
        os_kernel = splitted_data[1]

        return {
            "task": cls.hostnamectl.__name__,
            "data": [{"hostname": hostname, "os": os_version, "kernel": os_kernel}]
        }


# задаток
class SendToDatabase:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


class DataAccessLayerServer:
    @classmethod
    async def insert_server_data(cls, *args, **kwargs):
        pk = kwargs.get('target_pk')
        data = kwargs.get("data").get('data')[0]

        target = await models.Target.objects.aget(pk=pk)

        server_data, created = await models.ServerData.objects.aupdate_or_create(
            server_id_id=pk,
            defaults={
                "hostname": data.get('hostname'),
                "os": data.get('os'),
                "kernel": data.get('kernel'),
                "server_id": target,
            }
        )

        if not created:
            server_data.hostname = data.get('hostname'),
            server_data.os = data.get('os'),
            server_data.kernel = data.get('kernel'),
            server_data.record_date = timezone.now()
            await sync_to_async(server_data.save)()

        else:
            await sync_to_async(server_data.save)()

    @classmethod
    async def insert_cpu_data(cls, *args, **kwargs):
        pk = kwargs.get('target_pk')
        data = kwargs.get('data').get('data')[0].get('all_cores')
        cpu_cores = len(kwargs.get('data').get('data')[1].get('each_core'))

        target = await models.Target.objects.aget(pk=pk)

        q = await models.CPU.objects.acreate(
            cpu_user=data.get('us'),
            cpu_sys=data.get('sy'),
            cpu_nice=data.get('ni'),
            cpu_idle=data.get('id'),
            cpu_iowait=data.get('wa'),
            cpu_irq=data.get('hi'),
            cpu_softirq=data.get('si'),
            cpu_steal=data.get(' s'),
            cpu_cores=cpu_cores,
            cpu_util=data.get('cpu_load'),
            server_id=target
        )

        await sync_to_async(q.save)()

    @classmethod
    async def insert_ram_data(cls, *args, **kwargs):
        pass

    @classmethod
    async def insert_disk_data(cls, *args, **kwargs):
        pk = kwargs.get('target_pk')
        data = kwargs.get('data').get('data')

        target = await models.Target.objects.aget(pk=pk)

        for disk_data in data[:-6]:
            q = await models.DiskSpace.objects.acreate(
                file_system=disk_data.get('filesystem'),
                fs_size=disk_data.get('size'),
                fs_used=disk_data.get('used'),
                fs_avail=disk_data.get('available'),
                fs_used_prc=disk_data.get('use_percent')[:-1],
                mounted_on=disk_data.get('mounted_on'),
                record_date=timezone.now(),
                server_id=target
            )
            await sync_to_async(q.save)()

    @classmethod
    async def insert_net_data(cls, *args, **kwargs):
        pk = kwargs.get('target_pk')
        data = kwargs.get('data').get('data')

        target = await models.Target.objects.aget(pk=pk)

        for iface_data in data:
            q = await models.NetInterface.objects.acreate(
                interface=iface_data.get('iface'),
                status=iface_data.get('status'),
                ip_address=iface_data.get('ipaddress'),
                rx_bytes=float(iface_data.get('rx_bytes')[:-2]),
                rx_packets=iface_data.get('rx_packets'),
                rx_errors_errors=iface_data.get('rx_errors').get('errors'),
                rx_errors_dropped=iface_data.get('rx_errors').get('dropped'),
                rx_errors_overruns=iface_data.get('rx_errors').get('overruns'),
                rx_errors_frame=iface_data.get('rx_errors').get('frame'),
                tx_bytes=float(iface_data.get('tx_bytes')[:-2]),
                tx_packets=iface_data.get('tx_packets'),
                tx_errors_errors=iface_data.get('tx_errors').get('errors'),
                tx_errors_dropped=iface_data.get('tx_errors').get('dropped'),
                tx_errors_overruns=iface_data.get('tx_errors').get('overruns'),
                tx_errors_carrier=iface_data.get('tx_errors').get('carrier'),
                tx_errors_collisions=iface_data.get('tx_errors').get('collisions'),
                server_id=target
            )
            await sync_to_async(q.save)()
