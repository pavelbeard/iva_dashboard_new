import itertools
import socket
import ssl
from abc import ABC, abstractmethod
from collections import ChainMap

from dashboard.models import DashboardSettings


class PromDataHandler(ABC):
    GIBIBYTES = 1073741824

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def get_handled_data(self):
        pass


class CpuDataHandler(PromDataHandler, ABC):
    def __init__(self, data):
        super().__init__(data)

    def get_handled_data(self):
        result = self.data.get('data').get('result')

        handled_result = []

        for i in result:
            if i.get('metric').get('mode'):
                handled_result.append({
                    "mode": i['metric']['mode'],
                    "value": "{:.2f}".format(float(i['value'][1])).strip()
                })
            else:
                handled_result.append({
                    "coresCount": i['value'][1]
                })

        if len(handled_result) == 1:
            return {"data": handled_result}

        cpu_load = "{:.2f}".format(100 - float([i['value'] for i in handled_result if i['mode'] == 'idle'][0]))

        return {"data": handled_result, "cpuLoad": cpu_load}


class RamDataHandler(PromDataHandler):
    def __init__(self, data):
        super().__init__(data)

    def get_handled_data(self):
        for i in self.data.get('data').get('result'):
            value = 0 if len(i['value']) == 0 else "{:.2f}".format(float(i['value'][1]) / self.GIBIBYTES)
            metric = i['metric']['__name__'].split("_")[2].lower()
            return {"metric": metric, "value": value}


class FilesystemDataHandler(PromDataHandler):
    def __init__(self, data):
        super().__init__(data)

    def get_handled_data(self):
        handled_result = []

        for i in self.data.get('data').get('result'):
            tmp = i['value']
            i['value'] = "{:.2f}".format(float(tmp[1]) / self.GIBIBYTES)
            handled_result.append(i)

        return handled_result


class NetworkDataHandler(PromDataHandler):
    def __init__(self, data):
        super().__init__(data)

    def get_handled_data(self):
        handled_result = []

        for i in self.data.get('data').get('result'):
            if i.get('metric').get('__name__') == 'node_network_info':
                tmp = i['value'][1]
                i['value'] = tmp
                handled_result.append(i)
            else:
                tmp = i['value']
                i['value'] = "{:.2f}".format((float(tmp[1]) * 8) / 1024)
                handled_result.append(i)

        return handled_result


def get_ssl_cert():
    settings = DashboardSettings.objects.all().first()

    ssl_context = ssl.create_default_context()

    with socket.create_connection((settings.address_for_check_ssl, settings.port)) as sock:
        with ssl_context.wrap_socket(sock, server_hostname=settings.address_for_check_ssl) as ssock:
            issuer = dict(issuer={i[0]: i[1] for i in list(itertools.chain(*ssock.getpeercert()['issuer']))})
            valid_from = dict(validFrom=ssock.getpeercert()['notBefore'])
            valid_to = dict(validTo=ssock.getpeercert()['notAfter'])

            return dict(ChainMap(issuer, valid_from, valid_to))
