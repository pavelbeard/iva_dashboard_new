import asyncio
import json

from fastapi import FastAPI
from requests import Request
from starlette.responses import JSONResponse

from monitor_agent.agent import NoConnectionWithServer
from monitor_agent.agent import get_logger
from monitor_agent.dashboard import models
from monitor_agent.logic import exporter
from monitor_agent.logic.scraper import ScrapeLogic

logger = get_logger(__name__)

app = FastAPI()

exporters = [
    exporter.CPUDatabaseExporter(models.CPU).export,
    exporter.DatabaseExporter(models.RAM).export,
    exporter.DiskSpaceDatabaseExporter(models.DiskSpace, models.DiskSpaceStatistics).export,
    exporter.AdvancedDatabaseExporter(models.NetInterface).export,
    exporter.AdvancedDatabaseExporter(models.Process).export,
    exporter.DatabaseExporter(models.ServerData).export,
    exporter.DatabaseExporter(models.Uptime).export,
]

scraper_task = {}


@app.exception_handler(NoConnectionWithServer)
async def timeout_error(request: Request, exc: NoConnectionWithServer):
    return JSONResponse(
        status_code=408,
        content={"message": f"{exc.message}"}
    )


@app.on_event("startup")
async def start_scraping():
    sc = ScrapeLogic()
    scraper_task['task'] = asyncio.create_task(
        ScrapeLogic.scrape_forever(self=sc, exporters=exporters))


@app.on_event("shutdown")
async def stop_scraping():
    task = scraper_task['task']
    task.cancel("stopping task...")


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
    sc = ScrapeLogic()
    try:
        scrape_data = await sc.scrape_once()
        return JSONResponse(content=json.dumps(scrape_data), status_code=200)
    except Exception as e:
        logger.error(f"Exception {e.args[0]}")
        return JSONResponse(content={"message", "internal server error."}, status_code=500)


# задаток
@app.get("/api/monitor/metrics/target/{target_id: int}/cpu")
async def get_cpu_metrics(target_id: int) -> JSONResponse:
    pass
    # result = ScrapeLogic.get_data_from_target(target_id=target_id)
