import datetime
import uuid
from abc import ABC, abstractmethod

from monitor_agent.agent import get_logger
from monitor_agent.dashboard.models import ServerData, CPU, DiskSpace, DiskSpaceStatistics
from monitor_agent.logic.base import Exporter
from monitor_agent.logic.creator import insert_to_table, insert_all_to_table
from monitor_agent.logic.exceptions import ModelIsNotMatch
from monitor_agent.logic.reader import get_target, get_server_data
from monitor_agent.logic.updater import update_server_data

logger = get_logger(__name__)


class DatabaseExporter(Exporter, ABC):
    @staticmethod
    def get_address_port(target_id) -> str:
        target = get_target(target_id)
        return f"{target.address}:{target.port}"

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
        self.model = model

    def export(self, values, target_id):
        """
        Экспортирует метрики в postgresql.
        Для экспорта нужно прописать параметры model: Callable и values: dict
        """
        values |= self.uuid_record() | self.record_date() | self.t_id(target_id)

        insert_to_table(table=self.model, values=values)
        logger.info(f"Target data {self.get_address_port(target_id)} "
                    f"by model {self.model.__table__.name} has "
                    f"been added.")


class AdvancedDatabaseExporter(DatabaseExporter):
    def __init__(self, model):
        super().__init__(model)

    def export(self, values, target_id):
        """Экспортирует несколько записей за раз"""
        for value in values:
            value |= self.uuid_record() | self.record_date() | self.t_id(target_id)

        insert_all_to_table(self.model, values)
        logger.info(f"Target data {self.get_address_port(target_id)} "
                    f"by model {self.model.__table__.name} has "
                    f"been added.")


class CPUDatabaseExporter(DatabaseExporter):
    def __init__(self, model):
        if model is CPU:
            super().__init__(model)
        else:
            raise ModelIsNotMatch(CPU)

    def export(self, values, target_id):
        whole_processor_data = values.get('whole_processor_data')
        cpu_cores = len(values.get('processor_cores_data'))

        whole_processor_data |= self.uuid_record() | {
            "cpu_cores": cpu_cores
        } | self.record_date() | self.t_id(target_id)

        insert_to_table(table=self.model, values=whole_processor_data)
        logger.info(f"Target data {self.get_address_port(target_id)} "
                    f"by model {self.model.__table__.name} has "
                    f"been added.")


class DiskSpaceDatabaseExporter(DatabaseExporter):
    def __init__(self, model1, model2):
        if model1 is DiskSpace and model2 is DiskSpaceStatistics:
            super().__init__(model1)
            self.model2 = model2
        else:
            raise ModelIsNotMatch(DiskSpace, DiskSpaceStatistics)

    def export(self, values, target_id):
        for value in values:
            value |= self.uuid_record() | self.record_date() | self.t_id(target_id)

        insert_all_to_table(table=self.model, values=values[:-1])
        logger.info(f"Target data {self.get_address_port(target_id)} "
                    f"by model {self.model.__table__.name} has "
                    f"been added.")

        # export to diskspacestatistics
        insert_to_table(self.model2, values[-1])
        logger.info(f"Target data {self.get_address_port(target_id)} "
                    f"by model {self.model.__table__.name} has "
                    f"been added.")


class ServerDataDatabaseExporter(DatabaseExporter):
    def __init__(self, model):
        if model is ServerData:
            super().__init__(model)
        else:
            raise ModelIsNotMatch(ServerData)

    def export(self, values, target_id, **server_role):
        if isinstance(values, str):
            logger.error("values is not match a dict")
            return

        values |= self.t_id(target_id) | self.record_date() | server_role
        server_data = get_server_data(target_id)

        if not server_data:
            insert_to_table(table=self.model, values=values)
            logger.info(f"Target data {self.get_address_port(target_id)} "
                        f"by model {self.model.__table__.name} has "
                        f"been added.")

        else:
            update_server_data(self.model, target_id, values)
            logger.info(f"Updated target data {self.get_address_port(target_id)} "
                        f"by {self.model.__table__.name} model.")


class MonitoringServerExporter(Exporter, ABC):

    def export(self, **kwargs):
        pass
