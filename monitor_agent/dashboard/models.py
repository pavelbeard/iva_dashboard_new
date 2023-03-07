from sqlalchemy import Table

from monitor_agent.database.configuration import Base, metadata


class ScrapeCommand(Base):
    __table__ = Table('dashboard_scrapecommand', metadata)


class Target(Base):
    __table__ = Table('dashboard_target', metadata)


class DashboardSettings(Base):
    __table__ = Table('dashboard_dashboardsettings', metadata)


class CPU(Base):
    __table__ = Table('dashboard_cpu', metadata)


class RAM(Base):
    __table__ = Table('dashboard_ram', metadata)


class DiskSpace(Base):
    __table__ = Table('dashboard_diskspace', metadata)


# class DiskSpaceStatistics(Base):
#     __table__ = Table('dashboard_diskspacestatistics', metadata)


class NetInterface(Base):
    __table__ = Table('dashboard_netinterface', metadata)


class Process(Base):
    __table__ = Table('dashboard_process', metadata)


class ServerData(Base):
    __table__ = Table('dashboard_serverdata', metadata)


class Uptime(Base):
    __table__ = Table('dashboard_uptime', metadata)


class LoadAverage(Base):
    __table__ = Table('dashboard_loadaverage', metadata)
