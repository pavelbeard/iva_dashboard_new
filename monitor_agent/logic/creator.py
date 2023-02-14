from typing import Callable
import sqlalchemy.exc

from monitor_agent.agent import get_logger
from monitor_agent.db_connector.configuration import session

logger = get_logger(__name__)


def insert_to_table(table: Callable, values: dict):
    """
    Универсальный метод вставки строки в таблицы метрик.
    :param table: таблица для вставки
    :param values: данные для вставки
    :return: None
    """
    try:
        relation = table(**values)
        session.add(relation)
        session.commit()
    except sqlalchemy.exc.DataError as de:
        logger.error(f"DataError: msg{de.args[0]}")


def insert_all_to_table(table: Callable, values: list[dict] | tuple[dict]):
    """
    Универсальный метод вставки строк в таблицы метрик.
    :param table: таблица для вставки
    :param values: данные для вставки
    :return: None
    """
    try:
        relations = [table(**value) for value in values]
        session.add_all(relations)
        session.commit()
    except sqlalchemy.exc.DataError as de:
        logger.error(f"DataError: msg{de.args[0]}")

