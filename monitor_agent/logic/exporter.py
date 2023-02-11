import datetime
import uuid
from abc import ABC

from monitor_agent.agent import get_logger
from monitor_agent.logic.base import Exporter
from monitor_agent.logic.creator import insert_to_table, insert_all_to_table

logger = get_logger(__name__)


class DatabaseExporter(Exporter, ABC):
    @staticmethod
    def uuid_record() -> {}:
        return {"uuid_record": uuid.uuid4().hex}

    @staticmethod
    def record_date() -> {}:
        return {"record_date": datetime.datetime.now()}

    @staticmethod
    def t_id(target_id) -> {}:
        return {"target_id": target_id}

    def __init__(self, model):
        super().__init__(model)

    def export(self, values, target_id):
        """
        Экспортирует метрики в postgresql.
        Для экспорта нужно прописать параметры model: Callable и values: dict
        """
        values |= self.uuid_record() | self.record_date() | self.t_id(target_id)

        insert_to_table(table=self.model, values=values)
        logger.info(f"Data of {self.model.__table__.name} data was added to database.")


class AdvancedDatabaseExporter(DatabaseExporter):
    def __init__(self, model):
        super().__init__(model)

    def export(self, values, target_id):
        """Экспортирует несколько записей за раз"""
        for value in values:
            value |= self.uuid_record() | self.record_date() | self.t_id(target_id)

        insert_all_to_table(self.model, values)
        logger.info(f"Data of {self.model.__table__.name} data was added to database.")


class CPUDatabaseExporter(DatabaseExporter):
    def __init__(self, model):
        super().__init__(model)

    def export(self, values, target_id):
        whole_processor_data = values.get('whole_processor_data')
        cpu_cores = len(values.get('processor_cores_data'))

        whole_processor_data |= self.uuid_record() | {
            "cpu_cores": cpu_cores
        } | self.record_date() | self.t_id(target_id)

        insert_to_table(table=self.model, values=whole_processor_data)
        logger.info(f"Data of {self.model.__table__.name} data was added to database.")


class DiskSpaceDatabaseExporter(DatabaseExporter):
    def __init__(self, model1, model2):
        super().__init__(model1)
        self.model2 = model2

    def export(self, values, target_id):
        for value in values:
            value |= self.uuid_record() | self.record_date() | self.t_id(target_id)

        insert_all_to_table(table=self.model, values=values[:-1])
        logger.info(f"Data of {self.model.__table__.name} data was added to database.")

        # export to diskspacestatistics
        insert_to_table(self.model2, values[-1])
        logger.info(f"Data of {self.model2.__table__.name} data was added to database.")


class MonitoringServerExporter(Exporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def export(self, **kwargs):
        pass
