import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import AsyncGenerator

from asyncssh import PermissionDenied
from paramiko.ssh_exception import (AuthenticationException)

from monitor_agent.agent import get_logger
from monitor_agent.database.reader import (get_scrape_commands, get_settings,
                                           get_target, get_targets)
from monitor_agent.logic.extentions import row_2_dict

# TODO: отделить экспортер в БД от scraper'a

logger = get_logger(__name__)


class ValidationException(Exception):
    def __init__(self, message):
        self.message = message


class ScrapeLogic:
    def __init__(self, exporters, handlers, data_importer):
        """
        :param exporters: экспортеры данных. Любые.
            Главное, чтобы реализовывали интерфейс Exporter.
        :param handlers: обработчики данных с хостов.
        :param data_importer: поставщик данных с хостов.
        """
        self.exporters = exporters
        self.handlers = handlers
        self.data_importer = data_importer

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
    def _wrap_scraping_results(task_results, targets):
        """Генераторн"""
        for result, target in zip(task_results, targets):
            address = target.get('address')
            port = target.get('port')

            if isinstance(result, (AuthenticationException, PermissionDenied)):
                message = f"bad credentials: <host={address}, port={port}>."
                logger.error(message)
                yield message
            elif isinstance(result, TimeoutError):
                message = f"timeout error: <host={address}, port={port}>."
                logger.error(message)
                yield message
            elif isinstance(result, (OSError, ConnectionRefusedError)):
                message = f"unable to connect: <host={address}, port={port}>."
                logger.error(message)
                yield message
            elif isinstance(result, Exception):
                message = f"unexpected exception: {result}  <host={address}, port={port}>."
                logger.error(message)
                yield message
            else:
                logger.info(f"Target host {address}:{port} is scanned.")
                yield result

    async def arun_scraping(self, targets) -> ():
        """Асинхронная версия метода run_scraping."""
        callback = self.data_importer
        tasks = [asyncio.create_task(callback(
            target['address'],  # address
            target['port'],  # port
            target['username'],  # username
            target['password'],  # password
            target['commands'],  # commands
            5  # timeout
        )) for target in targets]

        tasks_results = await asyncio.gather(*tasks, return_exceptions=True)
        results = (result for result in self._wrap_scraping_results(tasks_results, targets))
        return results

    async def run_scraping(self, targets) -> ():
        """Запускает сбор метрик с целевых хостов в параллельном режиме."""
        try:
            with ProcessPoolExecutor(max_workers=3) as process_pool:
                loop = asyncio.get_running_loop()
                calls = [partial(  # args:
                    self.data_importer,  # func
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
            try:
                interval['value'] = int(get_settings().scrape_interval)
            except AttributeError:
                interval['value'] = 15

        results = await self.arun_scraping(targets)

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
