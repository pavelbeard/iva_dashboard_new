from sqlalchemy import select

from monitor_agent.dashboard.models import (DashboardSettings, ScrapeCommand,
                                            ServerData, Target)
from monitor_agent.database.configuration import session


# READ
def get_scrape_commands(record_id: int):
    scrape_commands = session.query(ScrapeCommand).filter(ScrapeCommand.record_id == record_id).first()
    return scrape_commands


def get_targets():
    statement = select(Target).where(Target.is_being_scan == True)
    query = session.scalars(statement)
    targets = [target for target in query]
    return targets


def get_target(target_id: int):
    target = session.query(Target).filter(Target.id == target_id).first()
    return target


def get_server_data(target_id: int):
    server_data = session.query(ServerData).filter(ServerData.target_id == target_id).first()
    return server_data


def get_settings():
    settings = session.query(DashboardSettings).filter(DashboardSettings.command_id == 1).first()
    return settings
