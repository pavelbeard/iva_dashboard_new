import asyncio
import json

from fastapi import FastAPI
from starlette.responses import JSONResponse

from monitor_agent import ioh
from monitor_agent.agent import get_logger
from http import HTTPStatus
from monitor_agent.logic.scraper import ScraperSetter, arun_scraping, get_data_from_targets
from monitor_agent.ssh.session import SSHSession

logger = get_logger(__name__)

app = FastAPI()

cache = {}


@app.on_event("startup")
async def start_scraping():
    _exporters_ = ioh.exporters_dict
    _handlers_ = ioh.handlers_dict

    ssh_session = SSHSession()
    scraper_builder = ScraperSetter()
    scraper = scraper_builder.allow_to_set_interval()\
        .set_exporters(tuple(_exporters_.values()))\
        .set_handlers(tuple(_handlers_.values()))\
        .set_data_scraper_callback(ssh_session.arun_cmd_on_target)\
        .set_scraper_cb(arun_scraping)\
        .get_data_from_targets(get_data_from_targets)\
        .build()

    cache['task'] = asyncio.create_task(scraper.scrape_forever())

    logger.info("Agent is run!")


@app.on_event("shutdown")
async def stop_scraping():
    logger.info("Agent is down.")
    task = cache['task']
    task.cancel()


@app.get("/api/monitor/ping")
async def ping() -> JSONResponse:
    """Проверка состояния агента """
    return JSONResponse(content={"ping": "ok"}, status_code=200)


@app.get("/api/monitor/metrics/targets/all")
async def get_all_metrics() -> JSONResponse:
    """
    Обратывает запрос на получение метрик из целевых хостов.
    Возвращает список кортежей: (target_id, data)
    :return: list[str | BaseException]
    """
    _exporters_ = tuple(ioh.exporters_dict.values())
    _handlers_ = tuple(ioh.handlers_dict.values())

    ssh_session = SSHSession()
    scraper_builder = ScraperSetter()
    scraper = scraper_builder.set_exporters(_exporters_)\
        .set_handlers(_handlers_)\
        .set_data_scraper_callback(ssh_session.arun_cmd_on_target)\
        .set_scraper_cb(arun_scraping)\
        .get_data_from_targets(get_data_from_targets)\
        .build()

    try:
        scrape_data = {}
        async for result in scraper.scrape_once():
            scrape_data |= result

        return JSONResponse(content=json.dumps(scrape_data), status_code=HTTPStatus.OK)
    except Exception as e:
        logger.error(f"Exception {e.args[0]}")
        return JSONResponse(
            content=json.dumps({"message", "internal server error."}),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
