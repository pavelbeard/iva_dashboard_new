import asyncio
import concurrent.futures
import os

import paramiko
import uvicorn
from asyncio.events import AbstractEventLoop
from functools import partial
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from .core import NoConnectionWithServer
from .core import app
from .core import run_cmd_on_target_host



origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://2.0.96.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type"],
)


# @app.on_event("startup")
@app.post("/api/monitor/metrics")
async def request_for_metrics(request: Request):
    """
    Обратывает запрос на получение метрик из целевых хостов
    :param request:
    :return:
    """
    body = await request.json()

    hosts = body.get('hosts')

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        calls: List[partial[tuple]] = [partial(run_cmd_on_target_host, host) for host in hosts]
        call_coros = [loop.run_in_executor(process_pool, call) for call in calls]

        task_results = await asyncio.gather(*call_coros, return_exceptions=True)
        results = []

        for result, host in zip(task_results, hosts):
            host, port, *_ = list(host.values())
            if isinstance(result, paramiko.ssh_exception.AuthenticationException):
                results.append({"message": f"bad credentials for {host}:{port}"})
            elif isinstance(result, type(paramiko.ssh_exception.SSHException)):
                results.append({"message": f"no connection to server: {host}:{port}"})
            else:
                results.append(result)

        return results


if __name__ == '__main__':
    host = os.getenv('MONITOR_AGENT_ADDRESS')
    port = os.getenv('MONITOR_AGENT_PORT')

    uvicorn.run(app="main:app", host=host, port=int(port), reload=True)
