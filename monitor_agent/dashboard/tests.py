import asyncio
import datetime
import uuid
from unittest import TestCase

from monitor_agent.dashboard.models import (CPU, RAM, DiskSpace,
                                            DiskSpaceStatistics, NetInterface,
                                            Process, ServerData, Uptime)
from monitor_agent.database import reader, creator
from monitor_agent.logic.exporters import (AdvancedDatabaseExporter,
                                           CPUDatabaseExporter,
                                           DatabaseExporter,
                                           DiskSpaceDatabaseExporter)
from monitor_agent.logic.extentions import row_2_dict
from monitor_agent.logic.scraper import ScrapeLogic


class TestModels(TestCase):
    def test_cpu_model(self):
        res = reader.get_scrape_commands()
        objs = [r for r in res]
        self.assertEqual(objs[0].target_id, 1)

    def test_get_target(self):
        res = reader.get_targets()
        objs = [r for r in res]
        self.assertEqual(reader.get_scrape_commands(objs[0].scrape_command_id).record_id, 0)

    def test_create_cpu(self):
        targets = reader.get_targets()

        targets_id = [row_2_dict(t) for t in targets]

        data = {
            "uuid_record": uuid.uuid4().hex,
            "cpu_cores": 16,
            "cpu_idle": 100.0,
            "cpu_iowait": 0.0,
            "cpu_irq": 0.0,
            "cpu_nice": 0.0,
            "cpu_softirq": 0.0,
            "cpu_steal": 0.0,
            "cpu_sys": 0.0,
            "cpu_user": 0.0,
            "cpu_util": 0.0,
            "record_date": datetime.datetime.now(),
            "target_id": targets_id[0].get('id')
        }

        creator.insert_to_table(CPU, data)
        pass

    def test_run_cmd_on_target(self):
        targets = [
            row_2_dict(target) | {"commands": row_2_dict(reader.get_scrape_commands(target.scrape_command_id))}
            for target in reader.get_targets()]

        host_address = True

        for n, target in enumerate(targets):
            target['address'] = "localhost"
            target['port'] = 2000 + n

        exporters = [
            CPUDatabaseExporter(CPU).export,
            DatabaseExporter(RAM).export,
            DiskSpaceDatabaseExporter(DiskSpace, DiskSpaceStatistics).export,
            AdvancedDatabaseExporter(NetInterface).export,
            AdvancedDatabaseExporter(Process).export,
            DatabaseExporter(ServerData).export,
            DatabaseExporter(Uptime).export,
        ]

        async def sub_test(exporters):

            sc = ScrapeLogic()
            results = await ScrapeLogic.run_scraping(sc, targets)
            self.assertEqual(type(results), list)

            for target, result in zip(targets, results):
                handle_results = ScrapeLogic.send_data_to_scrape_handler(result)

                for handle_result, ex in zip(handle_results, exporters):
                    ex(values=handle_result, target_id=target.get('id'))

                    # TODO: перенести в продакшн код
                    # TODO: доделать экспортеры
                    # TODO: перелопатить фронтенд
                    # TODO: приступить к chartJS

        asyncio.run(sub_test(exporters))
