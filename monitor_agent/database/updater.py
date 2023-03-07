from typing import Callable

import sqlalchemy.exc
from sqlalchemy import update, func, cast
from sqlalchemy.dialects.postgresql import JSONB

from monitor_agent.agent import get_logger
from monitor_agent.database.configuration import session

logger = get_logger(__name__)


def update_server_data(table: Callable, pk: int, values: dict):
    try:
        statement = update(table).values(
            **values).where(table.target_id == pk)
        session.execute(statement)
        session.commit()
    except sqlalchemy.exc.DataError as de:
        logger.error(f"DataError: msg{de.args[0]}")


def update_server_data_json(key, data, old_server_data):
    old_server_data = func.jsonb_set(
        cast(old_server_data, JSONB),
        key,
        cast(data, JSONB)
    )
    session.commit()