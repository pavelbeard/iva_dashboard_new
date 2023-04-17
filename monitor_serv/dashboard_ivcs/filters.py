import django_filters


class AuditLogRecordFilter(django_filters.FilterSet):
    date_created = django_filters.DateRangeFilter()
    severity = django_filters.NumberFilter()
    record_type = django_filters.NumberFilter()
    
