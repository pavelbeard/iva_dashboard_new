import ast
import json

import requests

from dashboard.models import Target


def dump(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


def scraped_data_handler(scraped_data):
    raw_json_data = ast.literal_eval(scraped_data)

    targets = {}

    for target_id, data in raw_json_data.items():
        target_obj = Target.objects.get(id=target_id)
        target_element_id = f"{target_obj.address.replace('.', '')}{target_obj.port}"

        targets.update({target_element_id: data})

    return json.dumps(targets, default=dump, indent=2)
