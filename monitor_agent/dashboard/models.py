from monitor_agent.db_connector.configuration import Base


class Target(Base):
    __table__ = Base.metadata.tables['dashboard_target']


class ServerData(Base):
    __table__ = Base.metadata.tables['dashboard_serverdata']


class DashboardSettings(Base):
    __table__ = Base.metadata.tables['dashboard_dashboardsettings']


class CPU(Base):
    __table__ = Base.metadata.tables['dashboard_cpu']


class RAM(Base):
    __table__ = Base.metadata.tables['dashboard_ram']


class DiskSpace(Base):
    __table__ = Base.metadata.tables['dashboard_diskspace']


class NetInterface(Base):
    __table__ = Base.metadata.tables['dashboard_netinterface']
