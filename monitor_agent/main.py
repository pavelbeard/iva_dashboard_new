import asyncio
import os

import uvicorn

from core import run_cmd_on_client
from core import app
from core import NoConnectionWithServer
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware

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


@app.on_event("startup")


@app.post("/api/monitor/metrics")
async def request_for_metrics(request: Request):
    body = await request.json()

    try:
        # TODO: опять здесь нужен сканкей


        result = await asyncio.wait_for(run_cmd_on_client(body), timeout=5)
        return result
    except TimeoutError:
        raise NoConnectionWithServer(body.get('host'), body.get('port'))


if __name__ == '__main__':
    host = os.getenv('MONITOR_AGENT_ADDRESS')
    port = os.getenv('MONITOR_AGENT_PORT')

    uvicorn.run(app="main:app", host=host, port=int(port), reload=True)
