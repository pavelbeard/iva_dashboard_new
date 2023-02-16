from abc import ABC, abstractmethod


class Exporter(ABC):
    """
    Базовый класс для экспорта данных в коллекторы данных.\n
    При наследовании соблюдать следующее соглашение:
        <МодельДанных><КоллекторДанных>Exporter
    """
    model = None

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def export(self, *args, **kwargs):
        """Экспортирует данные в указанное место"""
        pass


class CommandOutputHandlerBase(ABC):
    """
    Базовый класс для погдотовки данных комманд к экспорту в коллекторы данных.\n
    При наследовании соблюдать следующее соглашение:
        <МодельДанных><Команда>OutputHandler
    """
    @abstractmethod
    def handle(self, *args, **kwargs):
        """Обрабатывает данные к экспорту в коллекторы данных"""
        pass
