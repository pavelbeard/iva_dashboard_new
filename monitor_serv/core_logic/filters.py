from abc import ABC, abstractmethod
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from dateutil.relativedelta import relativedelta


class BaseDatetimeFilter(ABC):
    @abstractmethod
    def get_filter(self, *args, **kwargs):
        pass


class FilterByMinutes(BaseDatetimeFilter, ABC):
    @staticmethod
    def get_filter(minutes):
        return Q(record_date__gt=timezone.now() - timedelta(minutes=minutes))


class FilterByHours(BaseDatetimeFilter, ABC):
    @staticmethod
    def get_filter(hours):
        return Q(record_date__gt=timezone.now() - timedelta(hours=hours))


class FilterByDays(BaseDatetimeFilter, ABC):
    @staticmethod
    def get_filter(days):
        return Q(record_date__gt=timezone.now() - timedelta(days=days))


class FilterByMonths(BaseDatetimeFilter, ABC):
    @staticmethod
    def get_filter(months):
        return Q(record_date__gt=timezone.now() - relativedelta(months=months))


class FilterByYears(BaseDatetimeFilter, ABC):
    @staticmethod
    def get_filter(years):
        return Q(record_date__gt=timezone.now() - relativedelta(years=years))


class FilterByRange(BaseDatetimeFilter, ABC):
    @staticmethod
    def get_filter(start, end):
        return Q(record_date__range=(start, end))


class Filters(BaseDatetimeFilter):
    def __init__(self):
        self.filters = {}

    def update(self, **filter):
        self.filters.update(filter)

    def get_filter(self, filter_key, *args, **kwargs):
        return self.filters.get(filter_key)


filters_dict = Filters()
filters_dict.update(
    from1hour=FilterByHours.get_filter(1),
    from3hours=FilterByHours.get_filter(3),
    from6hours=FilterByHours.get_filter(6),
    from12hours=FilterByHours.get_filter(12),
    from1day=FilterByDays.get_filter(1),
    from1week=FilterByDays.get_filter(7),
    from1month=FilterByMonths.get_filter(1),
)
