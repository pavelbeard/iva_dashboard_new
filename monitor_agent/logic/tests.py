import asyncio
import datetime
import unittest

from monitor_agent.dashboard import models
from monitor_agent.dashboard.models import ServerData, LoadAverage
from monitor_agent.logic import creator, reader, updater, exporters, handle
from monitor_agent.logic.scraper import ScrapeLogic


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        server_role = exporters.ServerDataDatabaseExporter(models.ServerData).export
        cpu = exporters.CPUDatabaseExporter(models.CPU).export
        ram = exporters.DatabaseExporter(models.RAM).export
        fs = exporters.DiskSpaceDatabaseExporter(models.DiskSpace, models.DiskSpaceStatistics).export
        net = exporters.AdvancedDatabaseExporter(models.NetInterface).export
        apps = exporters.AdvancedDatabaseExporter(models.Process).export
        server_data = exporters.ServerDataDatabaseExporter(models.ServerData).export
        uptime = exporters.DatabaseExporter(models.Uptime).export
        load_average = exporters.DatabaseExporter(models.LoadAverage).export

        self.exporters = (server_role, cpu, ram, fs, net, apps, server_data, uptime, load_average)

        server_role = handle.CrmStatusOutputHandler()
        cpu = handle.CpuTopOutputHandler()
        ram = handle.RamFreeOutputHandler()
        fs = handle.DiskDfLsblkOutputHandler()
        net = handle.NetIfconfigOutputHandler()
        apps = handle.AppServiceStatusAllOutputHandler()
        server_data = handle.ServerDataHostnamectlOutputHandler()
        uptime = handle.UptimeUptimeOutputHandler()
        load_average = handle.LoadAverageUptimeOutputHandler()

        self.handlers = (server_role, cpu, ram, fs, net, apps, server_data, uptime, load_average)

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_scrape_logic(self):
        # async def scrape_logic_tst():
        #     await ScrapeLogic.scrape_forever()
        #
        # asyncio.run(scrape_logic_tst())
        pass

    def test_get_targets(self):
        result = reader.get_targets()
        [print(r.is_being_scan) for r in result]
        self.assertEqual(type(result), list)

    @staticmethod
    def test_create_and_update_server_data(self):
        pk = 17
        pk_name = "target_id"
        data = {
            "hostname": "hostname_test",
            "os": "Ubuntu 22.10.1 LTS",
            "kernel": "5.15.0-33.x86_64",
            "server_role": "media",
            "record_date": datetime.datetime.now()
        }

        from exporters import ServerDataDatabaseExporter

        exporter = ServerDataDatabaseExporter(ServerData)
        exporter.export(data, pk)

    def test_run_cmd_on_target(self):
        sc = ScrapeLogic()
        password = "Z0FBQUFBQmo2UUM5Q09FOTlZNWgtcEVmcjlRN0FwaUt5RG5Ub0h" \
                   "hbGtTTzV5aHYzTVgxMWJ4d0EwTmhfQWVOa2NKZWFiOEMwdmFndUc4ajNmTml5UlE3Yk9JT2tpelpMRmc9PQ=="
        commands = {"cpu": 'top -bn 1 -d.2 | grep "Cpu" && top 1 -w 70 -bn 1 | grep -P "^(%)"',
                    "record_id": 1,
                    "command": "sudo /usr/sbin/crm status"}

        address = "127.0.0.1"  # "192.168.248.5" # "127.0.0.1"
        port = 2000  # 9200 # 2000

        r = sc.run_cmd_on_target(address, port, "test", password, commands, 5)
        print(r)
        self.assertEqual(isinstance(r, dict), True)

    def test_scrape_forever(self):
        sc = ScrapeLogic(exporters=self.exporters, handlers=self.handlers)
        asyncio.run(sc.scrape_forever())

    def test_load_average_output_handler(self):
        r = handle.LoadAverageUptimeOutputHandler().handle("13:42:29 up"
                                                           "  5:22,  0 users,  load average: 0.07, 0.07, 0.09")
        self.assertEqual(isinstance(r, dict), True)

        target_id = 17
        exporters.DatabaseExporter(LoadAverage).export(r, 17)

    def test_async_ssh(self):
        async def asyncssh():
            sc = ScrapeLogic(self.exporters, self.handlers)

            password = "Z0FBQUFBQmo2UUM5Q09FOTlZNWgtcEVmcjlRN0FwaUt5RG5Ub0h" \
                       "hbGtTTzV5aHYzTVgxMWJ4d0EwTmhfQWVOa2NKZWFiOEMwdmFndUc4ajNmTml5UlE3Yk9JT2tpelpMRmc9PQ=="
            commands = {"cpu": 'top -bn 1 -d.2 | grep "Cpu" && top 1 -w 70 -bn 1 | grep -P "^(%)"',
                        "record_id": 1,
                        "command": "sudo /usr/sbin/crm status"}

            address = "127.0.0.1"  # "192.168.248.5" # "127.0.0.1"
            port = 2000  # 9200 # 2000

            cb = sc.arun_cmd_on_target

            tasks = [asyncio.create_task(cb(address, 2000, "test", password, commands, 5)),
                     asyncio.create_task(cb(address, 2001, "test1", password, commands, 5)),
                     asyncio.create_task(cb(address, 2002, "test2", password, commands, 5)),
                     asyncio.create_task(cb(address, 2003, "test", password, commands, 5))]

            res = await asyncio.gather(*tasks, return_exceptions=True)

            print(res)
            print(type(res))
            self.assertEqual(isinstance(res, list), True)

        asyncio.run(asyncssh())


if __name__ == '__main__':
    unittest.main()
