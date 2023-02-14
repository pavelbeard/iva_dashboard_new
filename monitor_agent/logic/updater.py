import sqlalchemy.exc
from sqlalchemy import update
from typing import Callable
from monitor_agent.agent import get_logger
from monitor_agent.db_connector.configuration import session

logger = get_logger(__name__)


def update_server_data(table: Callable, pk: int, values: dict):
    try:
        statement = update(table).values(
            **values).where(table.target_id == pk)
        session.execute(statement)
        session.commit()
    except sqlalchemy.exc.DataError as de:
        logger.error(f"DataError: msg{de.args[0]}")
