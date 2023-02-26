from sqlalchemy import URL, MetaData, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from monitor_agent import settings
from monitor_agent.agent import get_logger

###########################################################################################

###########################################################################################

###########################################################################################

logger = get_logger(__name__)

# database connection startup

DEBUG = bool(settings.DEBUG)

POSTGRES_DB_ADDRESS = settings.POSTGRES_DB_ADDRESS
POSTGRES_DB_PORT = settings.POSTGRES_DB_PORT
POSTGRES_DB_NAME = settings.POSTGRES_DB_NAME
POSTGRES_DB_USER = settings.POSTGRES_DB_USER
POSTGRES_DB_PASSWORD = settings.POSTGRES_DB_PASSWORD

DATABASE_URL = lambda driver: URL.create(
    drivername=f"postgresql+{driver}",
    username=POSTGRES_DB_USER,
    password=POSTGRES_DB_PASSWORD,
    host=POSTGRES_DB_ADDRESS,
    port=POSTGRES_DB_PORT,
    database=POSTGRES_DB_NAME
)

async_engine = create_async_engine(DATABASE_URL("asyncpg"), future=True)
engine = create_engine(DATABASE_URL("psycopg2"), future=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
session = scoped_session(sessionmaker(bind=engine))

# TODO: добавить в сервер мониторинга: импорт из бд
# TODO: изменить в сервер мониторинга: логику обработки данных из бд, refresher.js

Base = declarative_base()
metadata = MetaData()
metadata.reflect(bind=engine)

###########################################################################################

###########################################################################################

###########################################################################################
