import re

from monitor_agent.logic.base import CommandOutputHandlerBase
from monitor_agent.logic.extentions import DigitalDataConverters


class CpuTopOutputHandler(CommandOutputHandlerBase):
    @staticmethod
    def _cpu_analysis(cpu_data, core_num: int = None):
        """Вспомогательный метод обработки данных с процессора"""
        idle = cpu_data.get('id').strip()
        total = sum(map(lambda i: float(i), (v for v in cpu_data.values())))

        key = "cpu_util" if core_num is None else f"core{core_num}"

        if total != 0:
            cpu_data |= {key: f"{(1 - float(idle) / total) * 100:10.1f}".strip()}
        else:
            cpu_data |= {key: f"{(1 - float(idle)) * 100:10.2f}".strip()}

        return {
            "cpu_idle": cpu_data.get('id'),
            "cpu_iowait": cpu_data.get('wa'),
            "cpu_irq": cpu_data.get('hi'),
            "cpu_nice": cpu_data.get('ni'),
            "cpu_softirq": cpu_data.get('si'),
            "cpu_steal": cpu_data.get(' s'),
            "cpu_sys": cpu_data.get('sy'),
            "cpu_user": cpu_data.get('us'),
            "cpu_util": cpu_data.get('cpu_util'),
        }

    def handle(self, data: str):
        """
        Обрабатывает вывод команды:
        top -bn 1 -d.2 | grep "Cpu" && top 1 -w 70 -bn 1 | grep -P "^(%)"
        :param data: данные команды.
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no data."}
        elif 'no connection with server.' in data:
            return {"err_message": "connection error."}
        elif "command not found." in data:
            return {"err_message": "command not found."}

        processor, *cores = data.split("\n")
        processor_data = {i[-2:]: i[:-2] for i in re.split(",\s+|,", processor.split(":")[1].strip()[:-1])}
        cores_data = [{i[-2:]: i[:-2] for i in re.split(",\s+|,", x.split(":")[1].strip())} for x in cores[:-1]]

        whole_processor_data = self._cpu_analysis(cpu_data=processor_data)
        processor_cores_data = []

        for num, core in enumerate(cores_data):
            processor_cores_data.append(self._cpu_analysis(cpu_data=core, core_num=num))

        return {"cpu_data": {"whole_processor_data": whole_processor_data, "processor_cores_data": cores_data}}


class RamFreeOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str) -> {}:
        """
        Парсит информацию о загрузке RAM, всего RAM и свободной RAM на текущий момент.
        :param data: данные команды free -b.
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no_data."}
        elif "no connection with server." in data:
            return {"err_message": "connection error."}
        elif "command not found." in data:
            return {"err_message": "command not found."}

        ram_data = data.split("\n")
        # total used free shared buff/cache available
        ram_data = list(map(lambda x: re.split("\s+", x)[1:], ram_data[1:-1]))

        total_ram = ram_data[0][0]
        ram_used = ram_data[0][1]
        ram_free = ram_data[0][2]
        ram_shared = ram_data[0][3]
        ram_buff_cache = ram_data[0][4]
        ram_avail = ram_data[0][5]

        ram_util = f"{100 - (((float(ram_free) + float(ram_buff_cache)) * 100) / float(total_ram)):10.2f}".strip()

        # тут уже можно смело пересылать данные в бд
        return {
            "ram_data": {
                "total_ram": total_ram,
                "ram_used": ram_used,
                "ram_free": ram_free,
                "ram_shared": ram_shared,
                "ram_buff_cache": ram_buff_cache,
                "ram_avail": ram_avail,
                "ram_util": ram_util
            }
        }


class DiskDfLsblkOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str) -> {}:
        """
        Парсинг данных файловой системы с сервера.
        :param data: данные команды df -b и lsblk.
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no data."}
        elif "no connection with server." in data:
            return {"err_message": "connection error."}
        elif "command not found." in data:
            return {"err_message": "command not found."}

        fs_data = data.split("\n")
        disk_data = []
        # filesystem size used available use% mounted on
        for fs in fs_data[1:-2]:
            tmp_tuple = tuple(map(lambda x: x.strip(), fs.split()))
            file_system, fs_size, used, fs_avail, fs_used_prc, mounted_on = tmp_tuple
            disk_data.append({
                "file_system": file_system,
                "fs_size": fs_size,
                "fs_used": used,
                "fs_used_prc": fs_used_prc[:-1],
                "fs_avail": fs_avail,
                "mounted_on": mounted_on
            })

        most_valuable_partition = max(
            disk_data, key=lambda x: DigitalDataConverters.convert_metric_to_bytes(x.get('fs_size'))
        )

        disk_data += [{
            "total_disk_size": fs_data[-2].split()[3],
            "most_valuable_part_fs": most_valuable_partition.get('file_system'),
            "most_valuable_part_size": most_valuable_partition.get('fs_size'),
            "most_valuable_part_used": most_valuable_partition.get('fs_used'),
            "most_valuable_part_available": most_valuable_partition.get('fs_avail'),
            "most_valuable_part_use_percent": most_valuable_partition.get('fs_used_prc')
        }]

        return {"disk_data": disk_data}


class AppServiceStatusAllOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str) -> {}:
        """
        Парсит команду service --status-all.\n
        :param data: Данные, выведенные командой
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no data."}
        elif "no connection with server." in data:
            return {"err_message": "connection error."}
        elif "bad credentials." in data:
            return {"err_message": "bad credentials."}
        elif "command not found." in data:
            return {"err_message": "command not found."}

        other_data = data.split("\n")
        processes_list = []
        for d in other_data[:-1]:
            *status, process_name = d.split()
            status = str().join(status)

            process_status = "stopped" \
                if status == "[-]" else "running" \
                if status == "[+]" else "not determined"

            processes_list.append({
                "process_name": process_name, "process_status": process_status
            })

        return {"processes_list": processes_list}


class NetIfconfigOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str) -> {}:
        """
        Парсинг данных утилизации сетевых интерфейсов командой ifconfig.\n
        :param data: Данные команды ifconfig
        :return: {}
        """
        from ifconfigparser import IfconfigParser
        interfaces = IfconfigParser(data)

        net_data = []
        for i in interfaces.get_interfaces():
            iface = interfaces.get_interface(i)

            my_dict = {
                "interface": iface.name,
                "status": iface.state,
                "ip_address": DigitalDataConverters.from_cidr_to_prefixlen(
                    iface.ipv4_addr, iface.ipv4_mask
                ),
                "rx_bytes": iface.rx_bytes,
                "rx_packets": iface.rx_packets,
                "rx_errors_errors": iface.rx_errors,
                "rx_errors_dropped": iface.rx_dropped,
                "rx_errors_overruns": iface.rx_overruns,
                "rx_errors_frame": iface.rx_frame,
                "tx_bytes": iface.tx_bytes,
                "tx_packets": iface.tx_packets,
                "tx_errors_errors": iface.tx_errors,
                "tx_errors_dropped": iface.tx_dropped,
                "tx_errors_overruns": iface.tx_overruns,
                "tx_errors_carrier": iface.tx_carrier,
                "tx_errors_collisions": iface.tx_collisions
            }

            net_data.append(dict(
                map(lambda kv: (kv[0], 0) if kv[1] is None else (kv[0], kv[1]), my_dict.items())))

        return {"net_data": net_data}


class UptimeUptimeOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str) -> {}:
        """
        Показывает, сколько времени сервер находится в работе.
        :param data: данные команды uptime[uptime].
        :return: {}
        """
        if type(data) == dict:
            return {"no_data": "no_data"}
        elif "no connection with server." in data:
            return {"connection_error": True}
        elif "command not found." in data:
            return {"err_message": "command not found."}

        uptime_data = data.split("\n")

        return {"uptime": uptime_data[0].split(',')[0]}


class ServerDataHostnamectlOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str) -> {}:
        """
        Основные данные сервера: hostname, os_version, os_kernel и crm status.
        :param data: данные команды hostnamectl
        :return: {}
        """

        # костыль данных для замены команды crm status
        # data = data + settings.CRUTCH_DATA if settings.CRUTCH else ""

        if data == '':
            return {"err_message": "no_data"}

        splitted_data = data.split("\n")

        hostname = splitted_data[0]
        os_version = re.search("PRETTY_NAME=\"(.*)\"", data)[1]
        os_kernel = splitted_data[1]

        return {"hostname": hostname, "os": os_version, "kernel": os_kernel}


class CrmStatusOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str):
        try:
            hostname = re.search(r"\n(.*)\r$", data).group(1)
            current_dc = re.search(r"\s+Current\sDC:\s(.*)\s\(", data).group(1)
            server_role = "master" if current_dc == hostname else "slave"
        except AttributeError as e:
            server_role = "media"

        return {"server_role": server_role}


class LoadAverageUptimeOutputHandler(CommandOutputHandlerBase):
    def handle(self, data: str):
        """
        Парсинг данных о средней загрузки процессора за 1, 5 и 15 минут.
        :param data: данные команды uptime[load average].
        :return: {}
        """
        ONE_MIN, FIVE_MIN, FTEEN_MIN = re.findall("(\d+\.\d+)", data)
        return {"load_average_data": {"one_min": ONE_MIN, "five_min": FIVE_MIN, "fteen_min": FTEEN_MIN}}
