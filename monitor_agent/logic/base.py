from abc import ABC, abstractmethod


class ScraperDataAnalyserBase(ABC):
    @abstractmethod
    def cpu_analyser(self, data: str) -> {}:
        """
        Выводит информацию о загрузке процессора, количестве ядер и загрузку каждого ядра.\n
        :param data: Данные о загрузке процессора
        :return: {}
        """
        pass

    @abstractmethod
    def ram_analyser(self, data: str) -> {}:
        """
        Выводит информацию о загрузке RAM, всего RAM и свободной RAM на текущий момент
        :param data: RAM data
        :return: {}
        """
        pass

    @abstractmethod
    def filesystem_analyser(self, data: str) -> {}:
        """
        Анализ данных файловой системы с сервера
        :param data: Disk data
        :return: {}
        """
        pass

    @abstractmethod
    def net_analyser(self, data: str) -> {}:
        """
        Анализ утилизации сетевых интерфейсов командой ifconfig.\n
        :param data: Данные команды ifconfig
        :return: {}
        """
        pass

    @abstractmethod
    def app_analyser(self, data: str) -> {}:
        """
        Парсит unix-команду вывода списка приложений
        :param data: Данные, выведенные командой
        :return: {}
        """
        pass

    @abstractmethod
    def server_uptime(self, data: str):
        """
        Показывает, сколько времени сервер находится в работе.
        :param data: данные unix-команды.
        :return: {}
        """
        pass

    @abstractmethod
    def server_data(self, data: str):
        """
        Основные данные сервера: hostname, os_version, os_kernel.
        :param data: данные unix-команды.
        :return: {}
        """
        pass

    @abstractmethod
    def load_average(self, data: str):
        """
        Показывает среднюю загрузку сервера за 1, 5 и 15 минут.
        :param data: данные unix-команды
        :return:
        """


class Exporter(ABC):
    model = None

    @abstractmethod
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def export(self, *args, **kwargs):
        """Экспортирует данные в указанное место"""
        pass


class DataUnifier(ABC):
    """Класс для погдотовки данных к экспорту в коллекторы данных"""
    @abstractmethod
    def prepare_to_export(self, *args, **kwargs):
        """Погдотавливает данные к экспорту в коллекторы данных"""
        pass
