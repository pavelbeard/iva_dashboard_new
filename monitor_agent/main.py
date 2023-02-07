import asyncio
import concurrent.futures
import os
from asyncio.events import AbstractEventLoop
from functools import partial
from typing import List

import paramiko
import uvicorn

from agent import models
from agent import run_cmd_on_target_host, app, get_logger

logger = get_logger(__name__)


@app.on_event("startup")
async def scrape_metrics():
    asyncio.create_task()


@app.post("/api/monitor/metrics")
async def request_for_metrics(targets: models.Targets) -> list[str | BaseException]:
    """
    Обратывает запрос на получение метрик из целевых хостов
    :param targets: Целевые хосты
    :return: list[str | BaseException]
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as thread_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        calls: List[partial[tuple]] = [partial(run_cmd_on_target_host, host.dict(), 5) for host in targets.hosts]
        call_coros = [loop.run_in_executor(thread_pool, call) for call in calls]

        task_results = await asyncio.gather(*call_coros, return_exceptions=True)
        results = []

        for result, host in zip(task_results, targets.hosts):
            host, port, *_ = list(host.dict().values())

            if isinstance(result, paramiko.ssh_exception.AuthenticationException):
                results.append(f"{host}:{port}\nbad credentials.")
            elif isinstance(result, (
                    paramiko.ssh_exception.NoValidConnectionsError,
                    TypeError,
                    TimeoutError,
                    PermissionError,
                    OSError
            )):
                results.append(f"{host}:{port}\nno connection with server.")
            else:
                results.append(result)

        return results


if __name__ == '__main__':
    host = os.getenv('MONITOR_AGENT_ADDRESS')
    port = os.getenv('MONITOR_AGENT_PORT')

    uvicorn.run(app="main:app", host=host, port=int(port), reload=True)
