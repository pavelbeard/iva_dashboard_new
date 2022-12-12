import asyncio
import asyncssh
from monitor_srv.monitor_server.monitor_server.decorators import timed_lru_cache

# region NotUsed

# class OrStr(str):
#     def __init__(self, v: str):
#         self.v = v
#
#     def __or__(self, other):
#         return self.v if self.v != '' else other


# class ScankeyGenerator:
#     """Генерирует fingerprint для связи с сервером,
#     подлежащего мониторингу, по SSH"""
#
#     def __init__(self, data: dict):
#         """Принимает запрос от сервера мониторинга"""
#         self.__data = data
#
#     @timed_lru_cache(maxsize=12, seconds=21_600)
#     async def ssh_keyscan(self) -> {}:
#         """
#         Метод, генерирующий fingerprint для связи с сервером по SSH.\n
#         Использует встроенную утилиту ssh-keyscan.
#         :return: :{}: data
#         """
#         host = self.__data.get('host')
#         port = self.__data.get('port')
#
#         proc = await asyncio.subprocess.create_subprocess_shell(
#             f"ssh-keyscan -t rsa,dsa -p {port} {host}",
#             stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
#         )
#
#         stdout, stderr = await proc.communicate()
#
#         if len(stdout.decode('utf-8')) == 0:
#             raise NoKeyscanData(host, port)
#
#         key = asyncssh.import_known_hosts(stdout.decode('utf-8'))
#         self.__data.update({"key": key})
#         return self.__data
# endregion
