import asyncio
import re
import socket
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from logging import DEBUG
from typing import Type

import paramiko
from binascii import hexlify
from paramiko.ssh_exception import SSHException

from monitor_agent.agent import get_logger
from monitor_agent.logic.extentions import row_2_dict
from monitor_agent.logic.pass_handler import decrypt_pass
from monitor_agent.logic.reader import get_targets, get_settings, get_scrape_commands, get_target
from monitor_agent.logic.handle import ScrapedDataParser
from monitor_agent.settings import ENCRYPTION_KEY

# TODO: отделить экспортер в БД от scraper'a

logger = get_logger(__name__)


class ValidationException(Exception):
    def __init__(self, message):
        self.message = message


class AutoAddPolicy(paramiko.MissingHostKeyPolicy):
    """Класс, реализующий автодобавление открытых ключей с целевых хостов"""

    def missing_host_key(self, client, hostname, key):
        client._host_keys.add(hostname, key.get_name(), key)

        if client._host_keys_filename is not None:
            client.save_host_keys(client._host_keys_filename)

        client._log(DEBUG, f"Adding {key.get_name()} host key for {hostname}: "
                           f"{hexlify(key.get_fingerprint())}")


class ScrapeLogic:
    @staticmethod
    def get_data_from_targets() -> list:
        """Вытягивает данные целевых хостов из БД"""
        targets = [row_2_dict(target) | {"commands": row_2_dict(get_scrape_commands(target.scrape_command_id))}
                   for target in get_targets()]
        return targets

    @staticmethod
    def get_data_from_target(target_id: int):
        """Вытягивает данные с конкретного целевого хоста"""
        target = get_target(target_id=target_id)
        handle_target = row_2_dict(target) | {"commands": row_2_dict(get_scrape_commands(target.scrape_command_id))}
        return handle_target

    @staticmethod
    def send_data_to_scrape_handler(target_data: dict) -> list:
        """Соединяет данные с целевых хостов вместе и возвращает массив данных"""
        sdh = ScrapedDataParser()

        cpu = sdh.cpu_analyser(target_data.get('scrape_command_cpu'))
        ram = sdh.ram_analyser(target_data.get('scrape_command_ram'))
        fs = sdh.filesystem_analyser(target_data.get('scrape_command_fs'))
        net = sdh.net_analyser(target_data.get('scrape_command_net'))
        apps = sdh.app_analyser(target_data.get('scrape_command_apps'))
        server_data = sdh.server_data(target_data.get('scrape_command_hostnamectl'))
        uptime = sdh.server_uptime(target_data.get('scrape_command_uptime'))

        return [cpu, ram, fs, net, apps, server_data, uptime]

    async def run_scraping(self, targets) -> list:
        """Запускает сбор метрик с целевых хостов"""
        try:
            with ProcessPoolExecutor(max_workers=3) as process_pool:
                loop = asyncio.get_running_loop()
                calls = [
                    partial(  # args:
                        self.run_cmd_on_target,  # func
                        target['address'],  # address
                        target['port'],  # port
                        target['username'],  # username
                        target['password'],  # password
                        target['commands'],  # commands
                        5
                    )
                    for target in targets
                ]
                call_coros = [loop.run_in_executor(process_pool, call) for call in calls]

                task_results = await asyncio.gather(*call_coros, return_exceptions=True)

                results = []
                for result, target in zip(task_results, targets):
                    address = target.get('address')
                    port = target.get('port')

                    if isinstance(result, paramiko.ssh_exception.AuthenticationException):
                        results.append({"target": f"{address}:{port}", "message": "bad credentials."})
                    elif isinstance(result, (
                            paramiko.ssh_exception.NoValidConnectionsError,
                            TypeError,
                            TimeoutError,
                            PermissionError,
                            OSError
                    )):
                        results.append({"target": f"{address}:{port}", "message": "no connection with server."})
                    else:
                        logger.info(f"Target host {address}:{port} is scanned.")
                        results.append(result)

                return results
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    @staticmethod
    def run_cmd_on_target(
            address: str, port: int, username: str,
            password: str, commands: dict, timeout: int) -> dict | Type[SSHException]:
        """
        Запускает ssh-клиент, который в свою очередь, выполняет команды на целевом хосте.\n
        :param address: адрес целевого хоста.
        :param port: порт.
        :param username: имя пользователя для входа в систему.
        :param password: пароль.
        :param commands: команды для выполения на целевом хосте.
        :param timeout: Время ожидания соединения с сервером.
        :return: В случае успеха str, в случае, если учетные данные неправильные
        или нет связи с сервером - SSHException.
        """
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(AutoAddPolicy)
            decrypted_password = decrypt_pass(
                encryption_key=ENCRYPTION_KEY,
                password=password
            )
            commands.pop('record_id')

            try:
                client.connect(address, port, username, decrypted_password, timeout=timeout)

                result_dict = {}
                for key, command in commands.items():
                    if command != '':
                        stdin, stdout, stderr = client.exec_command(command, timeout * 2)

                        stderr_array = bytes.decode(stderr.read(), encoding='utf-8')

                        if len(stderr_array) != 0:
                            logger.warn(stderr_array)

                        result_dict[key] = bytes.decode(stdout.read(), encoding='utf-8')

                return result_dict

            except paramiko.ssh_exception.AuthenticationException:
                raise paramiko.ssh_exception.AuthenticationException
            except paramiko.ssh_exception.NoValidConnectionsError:
                raise paramiko.ssh_exception.NoValidConnectionsError
            except TimeoutError:
                raise TimeoutError
            except PermissionError:
                raise PermissionError
            except OSError:
                raise OSError

    async def scrape_once(self, set_interval: bool = False, interval=None, *args, **kwargs) -> list:
        """
        Метод, берущий метрики при каждом вызове метода.
        :param set_interval: устанавливается в True в том случае,
            если этот метод нужно вызвать несколько раз.
        :param interval: периодичность сбора метрик.
            используется вне метода, если его нужно вызывать несколько или бесконечное количество раз.
        """
        print()

        targets = self.get_data_from_targets()

        # так как словарь изменяемый объект, то при каждом
        # вытягивании значения интервала из БД словарь изменится.
        if set_interval:
            interval['value'] = int(get_settings().scrape_interval)

        results = await self.run_scraping(targets)

        targets_handled_data = []

        for target, result in zip(targets, results):
            if result.get('message') == 'bad credentials.':
                message = f"AuthenticationException: <{result.get('message')} address={target['address']}, " \
                          f"port={target['port']}>"
                targets_handled_data.append(message)
                logger.error(msg=message)
            elif result.get('message') == 'no connection with server.':
                message = f"OSError: <{result.get('message')} address={target['address']}, port={target['port']}>"
                targets_handled_data.append(message)
                logger.error(message)
            elif result.get('message') is None:
                targets_handled_data.append((target.get('id'), self.send_data_to_scrape_handler(result)))

        return targets_handled_data

    async def scrape_forever(self, exporters):
        """
        Бесконечный мониторинг серверов раз в interval.
        Интервал меняется в методе scrape_once.
        :param exporters: экспортеры данных. Любые.
            Главное, чтобы реализовывали интерфейс Exporter.
        """
        interval: dict = {"value": 5}  # интервал по умолчанию

        while True:
            try:
                targets_data = await self.scrape_once(interval=interval, set_interval=True)

                # export to db
                for target_data in targets_data:
                    if isinstance(target_data, tuple):
                        target_id, data = target_data
                        [ex(values=values, target_id=target_id) for values, ex in zip(data, exporters)]

            # пока не надо
            # except SSHException as e:
            #     logger.error(f"SSHException: {e.args[0]}")
            except KeyboardInterrupt as e:
                logger.error(f"KeyboardInterrupt: {e.args[0]}")
            except Exception as e:
                logger.error(f"Exception: {e.args[0]}")
            finally:
                await asyncio.sleep(interval.get('value'))
