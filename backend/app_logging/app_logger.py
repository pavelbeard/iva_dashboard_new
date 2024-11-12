import logging
import os
from logging import handlers

_logging_format = "[%(asctime)s] loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s"

APP_HOME = os.getenv("APP_HOME", os.getcwd())


def get_file_handler():
    # logs_path = os.path.join(os.getcwd(), "logs")
    #
    # if not os.path.exists(logs_path):
    #     os.mkdir(logs_path)
    #
    # fh = logging.handlers.RotatingFileHandler(os.path.join(APP_HOME, "logs", "monitor_server.log"), backupCount=10,
    #                                           maxBytes=1024 ** 2)
    fh = logging.StreamHandler()
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(_logging_format))
    return fh


def get_stream_handler():
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter(_logging_format))
    return sh


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
