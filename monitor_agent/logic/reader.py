from sqlalchemy import select
from monitor_agent.dashboard.models import (
    ScrapeCommand, Target,
    DashboardSettings)
from monitor_agent.db_connector.configuration import session


# READ
def get_scrape_commands(record_id: int):
    statement = select(ScrapeCommand).where(ScrapeCommand.record_id == record_id)
    scrape_commands = session.scalars(statement).one()
    return scrape_commands


def get_targets():
    statement = select(Target).where(Target.is_being_scan == True)
    query = session.scalars(statement)
    targets = [target for target in query]
    return targets


def get_target(target_id: int):
    statement = select(Target).where(Target.id == target_id)
    target = session.scalars(statement).one()
    return target


def get_settings():
    statement = select(DashboardSettings).where(DashboardSettings.command_id == 1)
    settings = session.scalars(statement).one()
    return settings
