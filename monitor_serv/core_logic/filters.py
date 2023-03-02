from abc import ABC, abstractmethod
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from dateutil.relativedelta import relativedelta


class BaseDatetimeFilter(ABC):
    @abstractmethod
    def get_filter(self, *args, **kwargs):
        pass

    @classmethod
    def _filters_dict(cls):
        return {mthd.__name__.split("By")[1].lower(): mthd.get_filter for mthd in cls.__subclasses__()}

    @classmethod
    def filter(cls, filter_id):
        return cls._filters_dict().get(filter_id)

    @classmethod
    def get_filter_list(cls, filter_keys_tuple):
        filter_dict = cls._filters_dict()
        return tuple([filter_dict.get(f) for f in filter_keys_tuple])


class FilterByMinutes(BaseDatetimeFilter, ABC):
    @staticmethod
    def get_filter(*args):
        return Q(record_date__gt=timezone.now() - timedelta(minutes=args[0]))


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
