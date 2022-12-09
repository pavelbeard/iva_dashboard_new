import asyncio
import subprocess
import unittest

import iva_dashboard

# from multiprocessing import ProcessError
from monitor_agent.core.handlers.data_handlers import ScankeyGenerator


class MonitorTests(unittest.TestCase):
    # def test_known_hosts_diff(self):
    #     async def main():
    #         with open('../../monitor_srv/hosts.yml', 'r') as hosts:
    #             tmp_hosts = yaml.safe_load(hosts).get('hosts')
    #
    #             hosts = [list(host.values())[1:] for host in tmp_hosts]
    #
    #             if not os.path.exists('../known_hosts'):
    #                 scan_hosts(hosts)
    #             else:
    #                 scan_hosts(hosts)
    #
    #             cmd = ['ps aux', 'netstat -tuna', 'ps']
    #
    #             tasks = [asyncio.wait_for(run_client(host, cmd), timeout=5) for host in hosts]
    #             results = await asyncio.gather(*tasks, return_exceptions=True)
    #
    #             for host, result in zip(tmp_hosts, results):
    #                 host, *tmp = host
    #                 if isinstance(result, TimeoutError):
    #                     print(f'\nTask for {host} failed: {result.__traceback__.tb_frame}', end='\n')
    #                     pass
    #                 elif isinstance(result, ProcessError):
    #                     print(f'Task for {host} exited with status: ProcessError={result.exit_status}')
    #                     pass
    #                 else:
    #                     print(f'\nTask for {host} succeeded:')
    #                     pass
    #
    #     asyncio.run(main())

    def test_known_hosts(self):
        async def run_client(host):
            async with iva_dashboard.connect(host="192.168.248.3", port=2249, username="pavelbeard",
                                             password="Rt3$YiOO",
                                             known_hosts=iva_dashboard.import_known_hosts(host)) as ssh:
                result = await ssh.run("uname -n")
                return result.stdout

        async def p():
            print("test_await")

        async def set_known_hosts():
            host = subprocess.run(
                "ssh-keyscan -t rsa,dsa -p 2249 192.168.248.3".split(), stdout=subprocess.PIPE
            ).stdout.decode('utf-8')

            tasks = [asyncio.wait_for(run_client(host), timeout=10) for i in range(5)]
            task1 = asyncio.create_task(p(), name="print await")
            # await asyncio.sleep(15)
            result = await asyncio.gather(*tasks, return_exceptions=True)
            assert type(result) == str

        asyncio.run(set_known_hosts())

    # def test_cache(self):
        # for i in range(100):
        #     start_time = time.time()
        #     result = ssh_keyscan("192.168.248.3", "2249")
        #     end_time = time.time() - start_time
        #     print(result, end_time)
            # print(ssh_keyscan.cache_info())

    def test_scankeys(self):
        test_set = [
            {"host": "192.168.248.3", "port": 2249, "username": "pavelbeard", "password": "Rt3$YiOO"},
            {"host": "192.168.248.4", "port": 2249, "username": "info-admin", "password": "Rt3$YiOO"},
        ]

        for el in test_set:
            skgen = ScankeyGenerator(data=el)
            test = skgen.ssh_keyscan()
            print(test)