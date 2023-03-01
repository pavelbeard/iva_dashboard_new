import ast
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


def get_data_from_targets():
    return [
        row_2_dict(target) | {
            "commands": ast \
                .literal_eval(get_scrape_commands(target.scrape_command_id) \
                              .scrape_command.replace('\r', ''))
        } for target in get_targets()
    ]


def get_data_from_target(target_id: int):
    """Вытягивает данные с конкретного целевого хоста"""
    target = get_target(target_id=target_id)
    return row_2_dict(target) | {
        "commands": row_2_dict(get_scrape_commands(target.scrape_command_id))
    }


async def arun_scraping(targets_data, data_scraper) -> ():
    """Асинхронная версия метода run_pool_scraping."""
    tasks = [asyncio.create_task(data_scraper(
        target['address'],  # address
        target['port'],  # port
        target['username'],  # username
        target['password'],  # password
        target['commands'],  # commands
        5  # timeout
    )) for target in targets_data]

    tasks_results = await asyncio.gather(*tasks, return_exceptions=True)
    return (result for result in ScrapedDataHandler.wrap_scraping_results(tasks_results, targets_data))


async def run_pool_scraping(targets_data, data_scraper) -> ():
    """Запускает сбор метрик с целевых хостов в параллельном режиме."""
    try:
        with ProcessPoolExecutor(max_workers=3) as process_pool:
            loop = asyncio.get_running_loop()
            calls = [partial(  # args:
                data_scraper,  # func
                target['address'],  # address
                target['port'],  # port
                target['username'],  # username
                target['password'],  # password
                target['commands'],  # commands
                5  # timeout
            ) for target in targets_data]

            call_coros = (loop.run_in_executor(process_pool, call) for call in calls)
            task_results = await asyncio.gather(*call_coros, return_exceptions=True)
            return (result for result in ScrapedDataHandler.wrap_scraping_results(task_results, targets_data))
    except KeyboardInterrupt:
        raise KeyboardInterrupt


class ScrapedDataHandler:
    """Вспомогательный класс для Scrapers"""

    @staticmethod
    def send_data_to_scrape_handler(target_data: dict, handlers) -> list:
        """Соединяет данные с целевых хостов вместе и возвращает массив данных"""
        results = []
        for values, instance in zip(list(target_data.values()), handlers):
            results.append(instance.handle(values))

        return results

    @staticmethod
    def wrap_scraping_results(task_results, targets):
        """Оборачивает результаты опроса в удобную форму для отсылки в коллектор данных"""
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


class ScraperLogic:
    def __init__(self):
        self.exporters = None
        self.handlers = None
        self.data_scraper_callback = None

        self.targets_data_callback = None
        self.target_data = None  # не реализован метод scrape_once_for_one_target

        self.allow_to_set_interval = None
        self.interval = 5

        self.run_scraping_cb = None

        self.scraping_results = None

    @staticmethod
    def new():
        return ScraperLogicBuilder()

    async def scrape_once(self) -> AsyncGenerator:
        """
        Метод, опрашивающий хосты при каждом вызове метода.
        """
        print()

        targets = self.targets_data_callback()

        # так как словарь изменяемый объект, то при каждом
        # вытягивании значения интервала из БД словарь изменится.
        if self.allow_to_set_interval:
            try:
                self.interval = int(get_settings().scrape_interval)
            except AttributeError:
                self.interval = 15

        results = await self.run_scraping_cb(targets, self.data_scraper_callback)

        for target, result in zip(targets, results):
            if isinstance(result, dict):
                yield {target.get('id'): ScrapedDataHandler.send_data_to_scrape_handler(
                    target_data=result, handlers=self.handlers)}
            else:
                yield {target.get('id'): result}

    async def scrape_forever(self):
        """
        Бесконечный мониторинг серверов раз в interval.
        Интервал меняется в методе scrape_once.
        """

        while True:
            try:
                # get data from hosts
                targets_data = self.scrape_once()

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
                await asyncio.sleep(self.interval)


class ScraperLogicBuilder:
    """Строитель класса ScraperLogic"""

    def __init__(self):
        self.scrape_logic = ScraperLogic()

    def build(self):
        return self.scrape_logic


class ScraperLogicExportersSetter(ScraperLogicBuilder):
    """1. Устанавливаем экспортеры данных"""

    def set_exporters(self, exporters):
        self.scrape_logic.exporters = exporters
        return self


class ScraperLogicHandlersSetter(ScraperLogicExportersSetter):
    """2. Устанавливаем обработчики данных с целевых хостов"""

    def set_handlers(self, handlers):
        self.scrape_logic.handlers = handlers
        return self


class ScraperLogicImporterSetter(ScraperLogicHandlersSetter):
    """3. Устанавливаем источник данных: ssh-scraper, victoria-metrics и тд."""

    def set_data_scraper_callback(self, data_scraper_callback):
        self.scrape_logic.data_scraper_callback = data_scraper_callback
        return self


class TargetsDataImport(ScraperLogicImporterSetter):
    """4. Данные для подключения к хостам - реализовывается в случае реализации ssh-клиента"""

    def get_data_from_targets(self, targets_data_callback):
        self.scrape_logic.targets_data_callback = targets_data_callback
        return self


class TargetDataImport(ScraperLogicBuilder):
    """4. Данные для подключения к хосту - реализовывается в случае реализации ssh-клиента"""

    def get_data_from_target(self, target_data_callback):
        """Вытягивает данные с конкретного целевого хоста"""
        self.scrape_logic.targets_data_callback = target_data_callback
        return self


class ScraperSettings(TargetsDataImport, TargetDataImport):
    """5. Если собираемся опросить хост 1 раз - не трогаем это."""

    def allow_to_set_interval(self):
        self.scrape_logic.allow_to_set_interval = True
        return self


class ScraperSetter(ScraperSettings):
    """6. Метод опроса хостов"""

    def set_scraper_cb(self, scraping_callback):
        self.scrape_logic.run_scraping_cb = scraping_callback
        return self
