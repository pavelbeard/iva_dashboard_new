import os
import yaml


def get_hosts(hosts_path: str):
    with open(hosts_path, 'r') as config:
        return yaml.safe_load(config).get('hosts')


def get_known_hosts(hosts_path: str):
    with open(hosts_path, 'r') as config:
        return yaml.safe_load(config).get('settings').get('known_hosts_location')
