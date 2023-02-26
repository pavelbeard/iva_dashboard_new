from abc import ABC, abstractmethod


class DataImporter(ABC):
    @abstractmethod
    def __init__(self, model=None, importer=None, *args, **kwargs):
        """
        Может принимать и django-модели, sqlalchemy-модели и тд.
        :param model:  какие данные модели (таблицы) импортировать.
        :param importer: строка подключения или что-то подобное
        """
        self.model = model
        self.importer = importer

    @abstractmethod
    def import_data(self, *args, **kwargs):
        """Метод импорта данных."""
        pass

