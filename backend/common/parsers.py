import re

from django.utils import timezone


def _status(status: str) -> tuple:
    match status:
        case "-":
            return "stopped", "0"
        case "+":
            return "running", "1"
        case _:
            return "unknown", "-1"


def service_status_all_parser(data: str, instance: str) -> dict:
    """
    :param data: данные команды service --status-all
    :param instance: сервер
    :return:
    """
    data = [re.split("\s\[\s|\s\]\s+", row)[1:] for row in data.split('\n') if row != '' or row != ' ']
    statuses = list(map(lambda x: {"service": x[-1], "status": _status(x[0])[0], "value": _status(x[0])[1]},
                        [d for d in data if len(d) > 1]))

    data = {
        "result": []
    }
    timestamp = timezone.now().timestamp()

    for s in statuses:

        data['result'].append({
            "metric": {
                "instance": instance,
                "__name__": s['service'],
                "status": s['status']
            },
            "value": [
                timestamp,
                s['value']
            ]
        })
    return data
