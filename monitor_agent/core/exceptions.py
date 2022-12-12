from starlette.responses import JSONResponse
from starlette.requests import Request
from .core import app


class NoConnectionWithServer(TimeoutError):
    def __init__(self, address: str, port):
        self.address = address
        self.port = port
        self.message = f"No connection to {address}:{port}. " \
                       f"Host is down or connection rejected by firewall!"


@app.exception_handler(NoConnectionWithServer)
async def timeout_error(request: Request, exc: NoConnectionWithServer):
    return JSONResponse(
        status_code=408,
        content={"message": f"{exc.message}"}
    )


# region Not Used
# class NoKeyscanData(Exception):
#     def __init__(self, address: str, port: str | int):
#         self.address = address
#         self.port = port
#         self.message = f"No key data from {address}:{port}. " \
#                        f"Host is down or connection rejected by firewall!"
#
#
# @app.exception_handler(NoKeyscanData)
# async def no_keyscan_data_exception_handler(request: Request, exc: NoKeyscanData):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"{exc.message}"}
#     )
# endregion
