import django_filters

from .models import AuditLogRecord


class AuditLogRecordFilter(django_filters.FilterSet):
    date_created = django_filters.DateTimeFromToRangeFilter()
    severity = django_filters.NumberFilter()
    record_type = django_filters.NumberFilter()

    class Meta:
        model = AuditLogRecord
        fields = ('date_created', 'severity', 'record_type')
        suffixes = {
            'min': 'after',
            'max': 'before'
        }
