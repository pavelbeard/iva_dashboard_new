import json
from http import HTTPStatus
from pprint import pprint
from urllib.parse import quote

from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class TestMixins(TestCase):
    fixtures = ["dashboardsets.json"]

    def setUp(self) -> None:
        self.CPU_DATA = {"querylist": json.dumps([
            {"label": "cpuData", "query": "query?query=(sum(irate(node_cpu_seconds_total[1h])) "
                                          "without (cpu) * 100) / count(node_cpu_seconds_total) without (cpu)"},
            {"label": "cpuCores", "query": "query?query=count(node_cpu_seconds_total{mode='idle'}) without (cpu, mode)"}
        ])}

        self.RAM_DATA = {"querylist": json.dumps([
            {"label": "memTotal", "query": "query?query=node_memory_MemTotal_bytes"},
            {"label": "buffers", "query": "query?query=node_memory_Buffers_bytes"},
            {"label": "slab", "query": "query?query=node_memory_Slab_bytes"},
            {"label": "memFree", "query": "query?query=node_memory_MemFree_bytes"},
            {"label": "memAvail", "query": "query?query=node_memory_MemAvailable_bytes"},
            {"label": "cached", "query": "query?query=node_memory_Cached_bytes"},
        ])}

        self.FS_DATA = {"querylist": json.dumps([
            {"label": "totalSpace", "query": "query?query=node_filesystem_size_bytes"},
            {"label": "usedSpace", "query": "query?query=node_filesystem_size_bytes-node_filesystem_free_bytes"},
            {"label": "reservedSpace", "query": "query?query=node_filesystem_free_bytes-node_filesystem_avail_bytes"},
            {"label": "freeSpace", "query": "query?query=node_filesystem_avail_bytes"},
        ])}

        self.NET_DATA = {"querylist": json.dumps([
            {"label": "throughputRX", "query": "query?query=node_network_receive_bytes_total"},
            {"label": "throughputTX", "query": "query?query=node_network_transmit_bytes_total"},
            {"label": "errorsRX", "query": "query?query=node_network_receive_errs_total"},
            {"label": "errorsTX", "query": "query?query=node_network_transmit_errs_total"},
            {"label": "packetsRX", "query": "query?query=node_network_receive_packets_total"},
            {"label": "packetsTX", "query": "query?query=node_network_transmit_packets_total"},
            {"label": "netState", "query": "query?query=node_network_info"},
        ])}

        self.ENCODED_NET_DATA = {"query": 'label_keep(('
                                          + 'alias(node_network_receive_errs_total, "RX errors"),'
                                          + 'alias(node_network_transmit_errs_total, "TX errors")' +
                                          '), "__name__", "device")'}
        self.THROUGHPUT = {
            "query": 'label_keep(('
                     + 'alias((rate(node_network_receive_bytes_total) * 8 / 1024), "RX"),'
                     + 'alias((rate(node_network_transmit_bytes_total) * 8 / 1024), "TX")'
                     + '), "__name__", "device")'
        }

        self.ROOT_SPACE = {
            "query": 'query?query=label_keep'
                     '(label_match('
                     '(alias('
                     '(node_filesystem_size_bytes-node_filesystem_free_bytes) / 1073741824, "Used"),'
                     ' alias((node_filesystem_free_bytes-node_filesystem_avail_bytes) / 1073741824, "Reserved"),'
                     ' alias(node_filesystem_avail_bytes / 1073741824, "Free")), "mountpoint", "/|/etc/hosts"),'
                     ' "__name__", "device")'
        }

    def test_response_data_mixin(self):
        response = self.client.get(reverse(
            "api:cpu_data",
            args=("127.0.0.1:9121",)))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ram_data(self):
        response = self.client.get(reverse(
            "api:ram_data",
            args=("127.0.0.1:9121",)))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_test_ssl_certs(self):
        response = self.client.get(reverse("api:ssl_test"))
        pprint(json.loads(response.content))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(isinstance(response.content, bytes))

    def test_filespace_data(self):
        response = self.client.get(reverse(
            "api:filesystem_data",
            args=("127.0.0.1:9121",)))
        pprint(json.loads(response.content), indent=3)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(isinstance(response.content, bytes))

    def test_network_data(self):
        response = self.client.get(reverse(
            "api:net_data", args=("127.0.0.1:9121",)))
        pprint(json.loads(response.content), indent=2, width=140, depth=5)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(isinstance(response.content, bytes))

    def test_encoded_network_data(self):
        self.THROUGHPUT['query'] = quote(self.THROUGHPUT['query'], safe='~@#$&()*!+=:;,?/\'')

        response = self.client.get(reverse(
            "api:net_data", args=("127.0.0.1:9101",)))
        pprint(json.loads(response.content), indent=2, width=140, depth=5)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(isinstance(response.content, bytes))

    def test_encoded_filesystem_data(self):
        self.ROOT_SPACE['query'] = quote(self.ROOT_SPACE['query'], safe='~@#$&()*!+=:;,?/\'')
        response = self.client.get(reverse(
            "api:filesystem_data", args=("127.0.0.1:9101",)))
        pprint(json.loads(response.content), indent=2, width=140, depth=5)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(isinstance(response.content, bytes))

