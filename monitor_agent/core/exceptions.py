import paramiko
from starlette.responses import JSONResponse
from starlette.requests import Request
from .application import app


class NoConnectionWithServer(paramiko.ssh_exception.SSHException):
    def __init__(self, address: str, port):
        self.address = address
        self.port = port
        self.message = f"No connection to {address}:{port}. " \
                       f"Host is down or connection rejected by firewall!"


# class IncorrectCredentials()


@app.exception_handler(NoConnectionWithServer)
async def timeout_error(request: Request, exc: NoConnectionWithServer):
    return JSONResponse(
        status_code=408,
        content={"message": f"{exc.message}"}
    )



