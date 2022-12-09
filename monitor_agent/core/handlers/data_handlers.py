import asyncio

from ..decorators import timed_lru_cache
from ..exceptions import NoKeyscanData


class OrStr(str):
    def __init__(self, v: str):
        self.v = v

    def __or__(self, other):
        return self.v if self.v != '' else other


class ScankeyGenerator:
    """Генерирует fingerprint для связи с сервером,
    подлежащего мониторингу, по SSH"""

    def __init__(self, data: dict):
        """Принимает запрос от сервера мониторинга"""
        self.__data = data

    @timed_lru_cache(maxsize=12, seconds=21_600)
    async def ssh_keyscan(self) -> {}:
        """
        Метод, генерирующий fingerprint для связи с сервером по SSH.\n
        Использует встроенную утилиту ssh-keyscan.
        :return: :{}: data
        """
        host = self.__data.get('host')
        port = self.__data.get('port')

        proc = asyncio.subprocess.create_subprocess_shell(
            f"ssh-keyscan -t rsa,dsa -p {port} {host}",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if len(stdout.decode('utf-8')) == 0:
            raise NoKeyscanData(host, port)

        key = asyncssh.import_known_hosts(stdout.decode('utf-8'))
        self.__data.update({"key": key})
        return self.__data


def systemctl_list_units_parser(data: str) -> {}:
    """
    Парсит команду systemctl list-units --type=service.\n
    :param hostname: Хост, на котором была вызвана команда
    :param data: Данные, выведенные командой
    :return: :{}:
    """
    hostname, *other_data = data.split("\n")

    tmp_list = []  # временный список для данных
    for row in other_data[1:-7]:
        tmp = row.split()[1:] + ['failed'] if "●" in row else row.split()
        unit, load, active, sub, *desc = tmp
        tmp_list.append({"unit": unit, "load": load, "active": active, "sub": sub})

    data_to_sent = {"hostname": hostname, "task": systemctl_list_units_parser.__name__, "data": tmp_list}
    return data_to_sent


def service_status_all(data: str) -> {}:
    """
    Парсит команду service --status-all.\n
    :param hostname: Хост, на котором была вызвана команда
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

    data_to_sent = {"hostname": hostname, "task": service_status_all.__name__, "data": tmp_list}
    return data_to_sent
