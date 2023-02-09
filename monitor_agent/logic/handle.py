import re
from abc import ABC

from monitor_agent.logic.base import ScraperDataAnalyserBase
from monitor_agent.logic.extentions import DigitalDataConverters


class ScrapedDataParser(ScraperDataAnalyserBase, ABC):
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

    def app_analyser(self, data: str) -> {}:
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

        return processes_list

    def cpu_analyser(self, data: str):
        """
        Парсит информацию о загрузке процессора, количестве ядер и загрузку каждого ядра.\n
        :param data: данные команды top 1 -kn
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no data."}
        elif 'no connection with server.' in data:
            return {"err_message": "connection error."}

        processor, *cores = data.split("\n")
        processor_data = {i[-2:]: i[:-2] for i in re.split(",\s+|,", processor.split(":")[1].strip()[:-1])}
        cores_data = [{i[-2:]: i[:-2] for i in re.split(",\s+|,", x.split(":")[1].strip())} for x in cores[:-1]]

        whole_processor_data = self._cpu_analysis(cpu_data=processor_data)
        processor_cores_data = []

        for num, core in enumerate(cores_data):
            processor_cores_data.append(self._cpu_analysis(cpu_data=core, core_num=num))

        return {"whole_processor_data": whole_processor_data, "processor_cores_data": cores_data}

    def ram_analyser(self, data: str) -> {}:
        """
        Парсит информацию о загрузке RAM, всего RAM и свободной RAM на текущий момент.
        :param data: данные команды free -b.
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no_data."}
        elif "no connection with server." in data:
            return {"err_message": "connection error."}

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
            "total_ram": total_ram,
            "ram_used": ram_used,
            "ram_free": ram_free,
            "ram_shared": ram_shared,
            "ram_buff_cache": ram_buff_cache,
            "ram_avail": ram_avail,
            "ram_util": ram_util
        }

    def filesystem_analyser(self, data: str) -> {}:
        """
        Парсинг данных файловой системы с сервера.
        :param data: данные команды df -b и lsblk.
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no data."}
        elif "no connection with server." in data:
            return {"err_message": "connection error."}

        fs_data = data.split("\n")
        part_fs_data = []
        # filesystem size used available use% mounted on
        for fs in fs_data[1:-2]:
            tmp_tuple = tuple(map(lambda x: x.strip(), fs.split()))
            file_system, fs_size, used, fs_avail, fs_used_prc, mounted_on = tmp_tuple
            part_fs_data.append({
                "file_system": file_system,
                "fs_size": fs_size,
                "fs_used": used,
                "fs_used_prc": fs_used_prc[:-1],
                "fs_avail": fs_avail,
                "mounted_on": mounted_on
            })

        most_valuable_partition = max(
            part_fs_data, key=lambda x: DigitalDataConverters.convert_metric_to_bytes(x.get('fs_size'))
        )

        part_fs_data += [{
            "total_disk_size": fs_data[-2].split()[3],
            "most_valuable_part_fs": most_valuable_partition.get('file_system'),
            "most_valuable_part_size": most_valuable_partition.get('fs_size'),
            "most_valuable_part_used": most_valuable_partition.get('fs_used'),
            "most_valuable_part_available": most_valuable_partition.get('fs_avail'),
            "most_valuable_part_use_percent": most_valuable_partition.get('fs_used_prc')
        }]

        return part_fs_data

    def net_analyser(self, data: str) -> {}:
        """
        Парсинг данных утилизации сетевых интерфейсов командой ifconfig.\n
        :param data: Данные команды ifconfig
        :return: {}
        """
        if type(data) == dict:
            return {"err_message": "no_data"}
        elif "no connection with server." in data:
            return {"err_message": "connection error."}
        elif data == [''] or data == '':
            return {"err_message": "command not found."}

        net_data = data.split("\n")
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

        net_data = []

        for interface in FORMAT_IFACES_INFO:
            interface, status, ip_address, netmask, \
                rx_bytes, rx_packets, rx_errors1, rx_errors2, rx_errors3, rx_errors4, \
                tx_bytes, tx_packets, tx_errors1, tx_errors2, tx_errors3, tx_errors4, tx_errors5 = interface
            net_data.append({
                "interface": interface,
                "status": status,
                "ip_address": DigitalDataConverters.from_cidr_to_prefixlen(
                    ip_address, netmask
                ),
                "rx_bytes": rx_bytes,
                "rx_packets": rx_packets,
                "rx_errors_errors": rx_errors1,
                "rx_errors_dropped": rx_errors2,
                "rx_errors_overruns": rx_errors3,
                "rx_errors_frame": rx_errors4,
                "tx_bytes": tx_bytes,
                "tx_packets": tx_packets,
                "tx_errors_errors": tx_errors1,
                "tx_errors_dropped": tx_errors2,
                "tx_errors_overruns": tx_errors3,
                "tx_errors_carrier": tx_errors4,
                "tx_errors_collisions": tx_errors5
            })

        return net_data

    def server_uptime(self, data: str) -> {}:
        """
        Показывает, сколько времени сервер находится в работе.
        :param data: данные команды uptime[uptime].
        :return: {}
        """
        if type(data) == dict:
            return {"no_data": "no_data"}
        elif "no connection with server." in data:
            return {"connection_error": True}

        uptime_data = data.split("\n")

        return {"uptime": uptime_data[0].split(',')[0]}

    def server_data(self, data: str) -> {}:
        """
        Основные данные сервера: hostname, os_version, os_kernel.
        :param data: данные команды hostnamectl
        :return: {}
        """

        if type(data) == dict:
            return {"no_data": "no_data"}

        splitted_data = data.split("\n")

        if "no connection with server." in data:
            return {"connection_error": True}

        hostname = splitted_data[0]
        os_version = re.search("PRETTY_NAME=\"(.*)\"", data)[1]
        os_kernel = splitted_data[1]

        return {"hostname": hostname, "os": os_version, "kernel": os_kernel}

    def load_average(self, data: str) -> {}:
        """
        Парсинг данных о средней загрузки процессора за 1, 5 и 15 минут.
        :param data: данные команды uptime[load average].
        :return: {}
        """
        pass
