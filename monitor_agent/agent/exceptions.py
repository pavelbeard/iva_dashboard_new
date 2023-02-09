import logging

import paramiko
from starlette.responses import JSONResponse
from starlette.requests import Request

logging.getLogger(__name__)


class NoConnectionWithServer(paramiko.ssh_exception.SSHException):
    def __init__(self, address: str, port):
        self.address = address
        self.port = port
        self.message = f"No connection to {address}:{port}. " \
                       f"Host is down or connection rejected by firewall!"


# class IncorrectCredentials()



