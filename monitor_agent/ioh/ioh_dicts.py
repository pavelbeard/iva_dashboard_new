from .exporters import *
from .handlers import *
from monitor_agent.dashboard import models

# exporters_dict = {
#     "server_role": ServerDataDatabaseExporter(models.ServerData).export,
#     "cpu": CPUDatabaseExporter(models.CPU).export,
#     "ram": DatabaseExporter(models.RAM).export,
#     "fs": DiskSpaceDatabaseExporter(models.DiskSpace, models.DiskSpaceStatistics).export,
#     "apps": AdvancedDatabaseExporter(models.Process).export,
#     "net": NetDataDatabaseExporter(models.NetInterface).export,
#     "server_data": ServerDataDatabaseExporter(models.ServerData).export,
#     "uptime": DatabaseExporter(models.Uptime).export,
#     "load_average": DatabaseExporter(models.LoadAverage).export,
# }
exporters_dict = {
    "server_role": ServerDataDatabaseExporter(models.ServerData).export,
    "cpu": JSONDataExporter(models.CPU).export,
    "ram": JSONDataExporter(models.RAM).export,
    "fs": JSONDataExporter(models.DiskSpace).export,
    "apps": JSONDataExporter(models.Process).export,
    "net": JSONDataExporter(models.NetInterface).export,
    "server_data": ServerDataDatabaseExporter(models.ServerData).export,
    "uptime": JSONDataExporter(models.Uptime).export,
    "load_average": JSONDataExporter(models.LoadAverage).export,
}

handlers_dict = {
    "server_role": CrmStatusOutputHandler(),
    "cpu": CpuTopOutputHandler(),
    "ram": RamFreeOutputHandler(),
    "fs": DiskDfLsblkOutputHandler(),
    "apps": AppServiceStatusAllOutputHandler(),
    "net": NetIfconfigOutputHandler(),
    "server_data": ServerDataHostnamectlOutputHandler(),
    "uptime": UptimeUptimeOutputHandler(),
    "load_average": LoadAverageUptimeOutputHandler(),
}


async def scan_for_plugins():
    pass
