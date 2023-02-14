import asyncio
import re
import socket
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from logging import DEBUG
from typing import Type, AsyncGenerator

import paramiko
import time
from binascii import hexlify
from paramiko.ssh_exception import SSHException, AuthenticationException, NoValidConnectionsError

from monitor_agent.agent import get_logger
from monitor_agent.logic import handle
from monitor_agent.logic.extentions import row_2_dict
from monitor_agent.logic.pass_handler import decrypt_pass
from monitor_agent.logic.reader import get_targets, get_settings, get_scrape_commands, get_target
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
    def __init__(self, exporters, handlers):
        """
        :param exporters: экспортеры данных. Любые.
            Главное, чтобы реализовывали интерфейс Exporter.
        :param handlers: обработчики данных с хостов.
        """
        self.exporters = exporters
        self.handlers = handlers

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

    def send_data_to_scrape_handler(self, target_data: dict) -> list:
        """Соединяет данные с целевых хостов вместе и возвращает массив данных"""
        results = [instance.handle(values) for values, instance in zip(list(target_data.values()), self.handlers)]
        return results

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
        result_dict = {}
        commands.pop('record_id')

        for key, command in commands.items():
            try:
                with paramiko.SSHClient() as client:
                    client.set_missing_host_key_policy(AutoAddPolicy)
                    decrypted_password = decrypt_pass(ENCRYPTION_KEY, password)

                    client.connect(address, port, username, decrypted_password, timeout=timeout)
                    stdin, stdout, stderr = client.exec_command(command, get_pty=True, timeout=timeout)

                    if "sudo" in command:
                        stdin.write(decrypted_password + "\n")
                        stdin.flush()

                    _out_ = stdout.read().decode('utf-8').replace(decrypted_password + "\r", "")
                    _err_ = stderr.read().decode('utf-8')

                    if len(_err_) > 0:
                        logger.warning(_err_)

                    result_dict[key] = _out_
            except TimeoutError as e:
                result_dict[key] = e
            except AuthenticationException:
                raise AuthenticationException
            except NoValidConnectionsError as e:
                raise OSError(e.errors)
            except OSError as e:
                result_dict[key] = e
            except Exception as e:
                result_dict[key] = e

        return result_dict

    @staticmethod
    def _wrap_scraping_results(task_results, targets):
        """Генераторн"""
        for result, target in zip(task_results, targets):
            address = target.get('address')
            port = target.get('port')

            if isinstance(result, AuthenticationException):
                message = f"bad credentials: <host={address}, port={port}>."
                logger.error(message)
                yield message
            elif isinstance(result, OSError):
                message = f"unable to connect: <host={address}, port={port}>."
                logger.error(message)
                yield message
            elif isinstance(result, Exception):
                message = f"unexpected exception: <host={address}, port={port}>."
                logger.error(message)
                yield message
            else:
                logger.info(f"Target host {address}:{port} is scanned.")
                yield result

    async def run_scraping(self, targets) -> ():
        """Запускает сбор метрик с целевых хостов в параллельном режиме."""
        try:
            with ProcessPoolExecutor(max_workers=3) as process_pool:
                loop = asyncio.get_running_loop()
                calls = [partial(  # args:
                    self.run_cmd_on_target,  # func
                    target['address'],  # address
                    target['port'],  # port
                    target['username'],  # username
                    target['password'],  # password
                    target['commands'],  # commands
                    5  # timeout
                ) for target in targets]

                call_coros = (loop.run_in_executor(process_pool, call) for call in calls)
                task_results = await asyncio.gather(*call_coros, return_exceptions=True)
                results = (result for result in self._wrap_scraping_results(task_results, targets))

                return results
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    async def scrape_once(self, set_interval: bool = False, interval=None, *args, **kwargs) -> AsyncGenerator:
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

        for target, result in zip(targets, results):
            if isinstance(result, dict):
                yield {target.get('id'): self.send_data_to_scrape_handler(result)}
            else:
                yield {target.get('id'): result}

    async def scrape_forever(self):
        """
        Бесконечный мониторинг серверов раз в interval.
        Интервал меняется в методе scrape_once.
        """
        interval: dict = {"value": 5}  # интервал по умолчанию

        while True:
            try:
                # get data from hosts
                targets_data = self.scrape_once(interval=interval, set_interval=True)

                # export to db
                async for target_data in targets_data:
                    target_id, data = iter(target_data.items()).__next__()
                    if isinstance(data, dict | list):
                        [ex(values=values, target_id=target_id) for values, ex in zip(data, self.exporters)]

            except KeyboardInterrupt as e:
                logger.error(f"KeyboardInterrupt: {e.args[0]}")
            except Exception as e:
                logger.error(f"Exception: {e.args[0]}", exc_info=True)
            finally:
                await asyncio.sleep(interval.get('value'))
