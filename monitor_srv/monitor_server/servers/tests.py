import asyncio
import unittest, yaml
from django.test import TestCase


# Create your tests here.

class Tests(unittest.TestCase):
    def test_write_yml(self):
        to_yaml = {
            "hosts": [
                {"address": "none", "port": 2249},
                {"address": "0.0.0.0", "port": 2245},
                {"address": "none", "port": 2241},
                {"address": "none", "port": 2230},
            ]
        }

        with open('test.yml', 'a') as f:
            yaml.dump(to_yaml, f)

    def test_interface_with_api(self):
        async def tst_interface_with_api():
            from logic.scrape_logic import IvaMetrics, IvaMetricsHandler

            scraper = IvaMetrics("C:\\Users\\pavel\\.iva_monitoring\\server_config.yml",
                                 "C:\\Users\\pavel\\.iva_monitoring\\iva_known_hosts")

            with open("C:\\Users\\pavel\\.iva_monitoring\\iva_known_hosts", 'r') as f:
                keys = f.read()

            ctx = [
                {"host": "localhost", "port": 2000, "username": "test",
                 "password": "test", "keys": keys,
                 "cmd": "service --status-all"},
                {"host": "localhost", "port": 2001, "username": "test",
                 "password": "test", "keys": keys,
                 "cmd": "service --status-all"},
            ]

            tasks = [scraper.scrape_metrics_from_agent(c) for c in ctx]
            results = await asyncio.gather(*tasks)

            assert type(results) == list

        asyncio.run(tst_interface_with_api())


class TestingViews(TestCase):
    def test_servers_processes_view(self):
        pass
