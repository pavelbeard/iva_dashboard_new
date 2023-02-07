import os
from monitor_agent import settings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

###########################################################################################

###########################################################################################

###########################################################################################

# database connection startup

POSTGRES_DB_ADDRESS = settings.POSTGRES_DB_ADDRESS
POSTGRES_DB_PORT = settings.POSTGRES_DB_PORT
POSTGRES_DB_NAME = settings.POSTGRES_DB_NAME
POSTGRES_DB_USER = settings.POSTGRES_DB_USER
POSTGRES_DB_PASSWORD = settings.POSTGRES_DB_PASSWORD

DATABASE_URL = lambda driver: f"postgresql+{driver}://{POSTGRES_DB_USER}:{POSTGRES_DB_PASSWORD}@" \
                              f"{POSTGRES_DB_ADDRESS}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}"

async_engine = create_async_engine(DATABASE_URL("asyncpg"), future=True, echo=settings.DEBUG)
engine = create_async_engine(DATABASE_URL("psycopg2"), future=True, echo=settings.DEBUG)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
session = scoped_session(sessionmaker(bind=engine))

# TODO: добавить в агент: экспорт в бд, endpoint состояния агента, импорт из бд настроек для агента,
#  логику обработки данных с хостов
# TODO: удалить из сервера мониторинга: экспорт в бд, логику обработки данных из агента мониторинга
# TODO: добавить в сервер мониторинга: импорт из бд
# TODO: изменить в сервер мониторинга: логику обработки данных из бд, refresher.js

Base = declarative_base()
Base.metadata.reflect(engine)

###########################################################################################

###########################################################################################

###########################################################################################
