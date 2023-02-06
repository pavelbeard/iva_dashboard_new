import logging
import os
from logging import handlers

_logging_format = "[%(asctime)s] loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s"


def get_file_handler():
    # fh = logging.handlers.RotatingFileHandler("logs/monitor_agent.log", backupCount=10,
    #                                           maxBytes=1024**2)
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
