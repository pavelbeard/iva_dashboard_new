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


class ModelIsNotMatch(Exception):
    def __init__(self, expected_model1, expected_model2=None):
        if expected_model2 is None:
            self.message = f"Входящая модель не соответствует ожидаемой. Ожидаемая модель: {expected_model1}"
        else:
            self.message = f"Входящие модели не соответствуют ожидаемым. " \
                           f"Ожидаемые модели: {expected_model1}, {expected_model2}"

# class IncorrectCredentials()



