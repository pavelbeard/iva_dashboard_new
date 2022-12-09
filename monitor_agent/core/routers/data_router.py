import asyncio

import asyncssh
from starlette.responses import JSONResponse
from fastapi import APIRouter
from starlette.requests import Request

from ..core import app
from ..exceptions import NoKeyscanData, NoConnectionWithServer
from ..ssh_client.ssh_client import run_client
from ..handlers import data_handlers

router = APIRouter()


@app.exception_handler(NoKeyscanData)
async def no_keyscan_data_exception_handler(request: Request, exc: NoKeyscanData):
    return JSONResponse(
        status_code=418,
        content={"message": f"{exc.message}"}
    )


@app.exception_handler(NoConnectionWithServer)
async def timeout_error(request: Request, exc: NoConnectionWithServer):
    return JSONResponse(
        status_code=408,
        content={"message": f"{exc.message}"}
    )


@router.post("/api/monitor/systemctl-services")
async def request_for_systemctl_services(request: Request):
    data = await request.json()

    try:
        raw_data = await asyncio.wait_for(run_client(data, "uname -n && systemctl list-units --type=service"),
                                          timeout=5)
    except TimeoutError:
        raise NoConnectionWithServer(data.get('host'), data.get('port'))

    response = data_handlers.systemctl_list_units_parser(raw_data)

    return response


@router.post("/api/monitor/services-status-all")
async def request_for_systemctl_services(request: Request):
    data = await request.json()

    try:
        raw_data = await asyncio.wait_for(run_client(data, "uname -n && service --status-all"), timeout=5)
    except TimeoutError:
        raise NoConnectionWithServer(data.get('host'), data.get('port'))

    response = data_handlers.service_status_all(raw_data)

    return response
