import asyncio

import uvicorn

from .core import run_cmd_on_client
from .core import app
from .core import NoConnectionWithServer
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


@app.post("/api/monitor/metrics")
async def request_for_metrics(request: Request):
    body = await request.json()

    try:
        result = await asyncio.wait_for(run_cmd_on_client(body), timeout=5)
        return result
    except TimeoutError:
        raise NoConnectionWithServer(body.get('host'), body.get('port'))


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080, reload=True)
