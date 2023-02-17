import asyncio
import json

from fastapi import FastAPI
from starlette.responses import JSONResponse

from monitor_agent.agent import get_logger
from monitor_agent.dashboard import models
from monitor_agent.logic import exporters, handle
from monitor_agent.logic.scraper import ScrapeLogic

logger = get_logger(__name__)

app = FastAPI()

scraper_task = {}
exporters_dict = {}
handlers_dict = {}


@app.on_event("startup")
async def start_scraping():
    server_role = handle.CrmStatusOutputHandler()
    cpu = handle.CpuTopOutputHandler()
    ram = handle.RamFreeOutputHandler()
    fs = handle.DiskDfLsblkOutputHandler()
    net = handle.NetIfconfigOutputHandler()
    apps = handle.AppServiceStatusAllOutputHandler()
    server_data = handle.ServerDataHostnamectlOutputHandler()
    uptime = handle.UptimeUptimeOutputHandler()
    load_average = handle.LoadAverageUptimeOutputHandler()

    _handlers_ = (server_role, cpu, ram, fs, net, apps, server_data, uptime, load_average)

    server_role = exporters.ServerDataDatabaseExporter(models.ServerData).export
    cpu = exporters.CPUDatabaseExporter(models.CPU).export
    ram = exporters.DatabaseExporter(models.RAM).export
    fs = exporters.DiskSpaceDatabaseExporter(models.DiskSpace, models.DiskSpaceStatistics).export
    net = exporters.AdvancedDatabaseExporter(models.NetInterface).export
    apps = exporters.AdvancedDatabaseExporter(models.Process).export
    server_data = exporters.ServerDataDatabaseExporter(models.ServerData).export
    uptime = exporters.DatabaseExporter(models.Uptime).export
    load_average = exporters.DatabaseExporter(models.LoadAverage).export

    _exporters_ = (server_role, cpu, ram, fs, net, apps, server_data, uptime, load_average)

    sc = ScrapeLogic(exporters=_exporters_, handlers=_handlers_)
    scraper_task['task'] = asyncio.create_task(sc.scrape_forever())
    exporters_dict['exporters'] = _exporters_
    handlers_dict['handlers'] = _handlers_
    logger.info("Agent is run!")


@app.on_event("shutdown")
async def stop_scraping():
    logger.info("Agent is down.")
    task = scraper_task['task']
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
    sc = ScrapeLogic(
        exporters=iter(exporters_dict.values()).__next__(),
        handlers=iter(handlers_dict.values()).__next__()
    )
    try:
        scrape_data = {}
        async for result in sc.scrape_once():
            scrape_data |= result

        return JSONResponse(content=json.dumps(scrape_data), status_code=200)
    except Exception as e:
        logger.error(f"Exception {e.args[0]}")
        return JSONResponse(content=json.dumps({"message", "internal server error."}), status_code=500)


# задаток
@app.get("/api/monitor/metrics/target/{target_id: int}/cpu")
async def get_cpu_metrics(target_id: int) -> JSONResponse:
    pass
    # result = ScrapeLogic.get_data_from_target(target_id=target_id)
