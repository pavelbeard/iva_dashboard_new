import uuid
from random import choice

from django.db.models import Q

COLOR_PALETTE = (
    "966B9D", "C98686", "F2B880", "FFF4EC",
    "E7CFBC", "D1BCE3", "C49BBB", "585481",
    "19297C", "041B15", "136F63", "22AAA1",
    "4CE0D2", "84CAE7", "FFBE0B", "FB5607",
    "FF006E", "8338EC", "3A86FF", "3A86FF",
)


def create_chart_data(model, keys, target_id, filter, *args, **kwargs):
    datasets = []

    query = model \
        .objects \
        .filter(Q(target_id=target_id) & filter()) \
        .order_by("-record_date")

    for num, key in enumerate(keys):
        datasets.append({
            "label": key,
            "backgroundColor": "#" + COLOR_PALETTE[num],
            "data": list(map(lambda i: getattr(i, key), query)),
        })
    else:
        labels = list(map(lambda i: getattr(
            i, "record_date").__format__("%d/%m/%y %H:%M:%S"), query))

    return {
        "labels": labels,
        "datasets": datasets
    }
