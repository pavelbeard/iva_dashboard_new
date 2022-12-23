import paramiko
import uvicorn
import asyncio
import concurrent.futures
import os

from typing import List
from asyncio.events import AbstractEventLoop
from functools import partial
from starlette.requests import Request
from agent import run_cmd_on_target_host, app, get_logger


logger = get_logger(__name__)


# TODO: нужна валидация модели
@app.post("/api/monitor/metrics")
async def request_for_metrics(request: Request):
    """
    Обратывает запрос на получение метрик из целевых хостов
    :param request:
    :return:
    """
    body = await request.json()

    hosts = body.get('hosts')

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as thread_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        calls: List[partial[tuple]] = [partial(run_cmd_on_target_host, host, 5) for host in hosts]
        call_coros = [loop.run_in_executor(thread_pool, call) for call in calls]

        task_results = await asyncio.gather(*call_coros, return_exceptions=True)
        results = []

        for result, host in zip(task_results, hosts):
            host, port, *_ = list(host.values())

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
