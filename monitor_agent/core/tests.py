import asyncio
import concurrent.futures
import copyreg
import multiprocessing
import pickle
import subprocess
import types
import unittest
from binascii import hexlify
from functools import partial
from logging import DEBUG
from typing import List

import iva_dashboard
import paramiko


# from multiprocessing import ProcessError
# from monitor_agent.core.handlers.data_handlers import ScankeyGenerator

class AutoAddPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        client._host_keys.add(hostname, key.get_name(), key)

        if client._host_keys_filename is not None:
            client.save_host_keys(client._host_keys_filename)

        client._log(DEBUG, f"Adding {key.get_name()} host key for {hostname}: "
                           f"{hexlify(key.get_fingerprint())}")


class MonitorTests(unittest.TestCase):
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

    def test_redis(self):
        async def test_redis_async():
            from . import redis
            redis = redis.RedisClient()

    def test_load_host_keys(self):
        pass


def many_clients(conn_data: tuple):
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy)
        hostname, port, username, password = conn_data

        try:
            client.connect(hostname, port, username, password)
            stdin, stdout, stderr = client.exec_command("service --status-all")
            return bytes.decode(stdout.read(), encoding='utf-8')

        except paramiko.SSHException as err:
            return err


async def main():
    test_set = [
        ("localhost", 2000, "test", "test"),
        ("localhost", 2001, "test", "test"),
        ("localhost", 2002, "test", "test"),
        ("localhost", 2003, "test", "test"),
        ("localhost", 2004, "test", "test"),
        ("localhost", 2005, "test", "test"),
    ]

    with concurrent.futures.ProcessPoolExecutor() as process_pool:
        loop = asyncio.get_running_loop()
        calls: List[partial[tuple]] = [partial(many_clients, host) for host in test_set]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*call_coros)

        for result in results:
            print(result)


if __name__ == '__main__':
    asyncio.run(main())
