import asyncio
import subprocess
import unittest

import asyncssh

# from multiprocessing import ProcessError
# from monitor_agent.core.handlers.data_handlers import ScankeyGenerator


class MonitorTests(unittest.TestCase):
    def test_known_hosts(self):
        async def run_client(host):
            async with asyncssh.connect(host="192.168.248.3", port=2249, username="pavelbeard",
                                             password="Rt3$YiOO",
                                             known_hosts=asyncssh.import_known_hosts(host)) as ssh:
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