from abc import ABC
from datetime import timedelta, datetime
from functools import partial

from django.utils import timezone

from app_logging.app_logger import get_logger
from core_logic.base import DataImporter
from core_logic.chart import create_chart_data
from core_logic.filters import BaseDatetimeFilter

logger = get_logger(__name__)


class DjangoORMImporter(DataImporter, ABC):
    def __init__(self, model):
        super().__init__(model)
        self.filter = BaseDatetimeFilter.filter


class CPUDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, filter_key, time_value, *args, **kwargs):
        keys = ["cpu_idle", "cpu_iowait", "cpu_irq", "cpu_nice", "cpu_softirq",
                "cpu_steal", "cpu_sys", "cpu_user"]

        Qfilter = partial(self.filter(filter_key), time_value)

        data = create_chart_data(self.model, keys, target_id, Qfilter, args, kwargs)

        return {
            "chartData": data,
            "target_id": target_id,
        }


class RAMDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, filter_key, time_value, *args, **kwargs):
        keys = [["total_ram"], ["ram_used", "ram_free", "ram_shared",
                                "ram_buff_cache", "ram_avail"]]

        data = []

        Qfilter = partial(self.filter(filter_key), time_value)

        for nested_keys in keys:
            data.append(create_chart_data(self.model, nested_keys, target_id, Qfilter, *args, **kwargs))

        return {
            "chartData": data,
            "target_id": target_id,
        }


class DiskDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, *args, **kwargs):
        chart_data = []

        query = self.model.objects.filtered_query(
            target_id=target_id,
            record_date__gt=timezone.now() - timedelta(minutes=15)
        ).order_by("-record_date")

        for obj in self.model.objects.filtered_query(target_id=target_id).order_by("-record_date")[:50]:
            chart_data.append({
                "filesystem": obj.file_system,
                "fsSize": obj.fs_size,
                "fsUsed": obj.fs_used,
                "fsAvail": obj.fs_avail,
                "recordDates": obj.record_date.__format__("%d/%m/%y %H:%M:%S"),
            })

        return {
            "chartDataKeys": [k for k in chart_data[0]],
            "chartData": chart_data,
            "target_id": target_id,
        }


class NetDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, *args, **kwargs):
        chart_data = []

        query = self.model.objects.filtered_query(
            target_id=target_id,
            record_date__gt=datetime.now() - timedelta(minutes=15))

        ifaces_ids = [
            i[0] for i in
            self.model.objects.filtered_query(target_id=target_id).values_list('interface_id').distinct()
        ]

        ifaces_names = [
            self.model.objects.filtered_query(target_id=target_id, interface_id=iface_id).first().interface
            for iface_id in ifaces_ids
        ]

        distributed_data = []
        for iface_id, iface_name in zip(ifaces_ids, ifaces_names):
            rx_bytes_data = []
            rx_packets_data = []
            rx_errors_errors_data = []
            rx_errors_dropped_data = []
            rx_errors_overruns_data = []
            rx_errors_frame_data = []
            tx_bytes_data = []
            tx_packets_data = []
            tx_errors_errors_data = []
            tx_errors_dropped_data = []
            tx_errors_overruns_data = []
            tx_errors_carrier_data = []
            tx_errors_collisions_data = []
            record_dates = []

            for i in self.model.objects.filtered_query(target_id=target_id, interface_id=iface_id).order_by(
                    "-record_date")[
                     :50]:
                rx_bytes_data.append(i.rx_bytes)
                rx_packets_data.append(i.rx_packets)
                rx_errors_errors_data.append(i.rx_errors_errors)
                rx_errors_dropped_data.append(i.rx_errors_dropped)
                rx_errors_overruns_data.append(i.rx_errors_overruns)
                rx_errors_frame_data.append(i.rx_errors_frame)
                tx_bytes_data.append(i.tx_bytes)
                tx_packets_data.append(i.tx_packets)
                tx_errors_errors_data.append(i.tx_errors_errors)
                tx_errors_dropped_data.append(i.tx_errors_dropped)
                tx_errors_overruns_data.append(i.tx_errors_overruns)
                tx_errors_carrier_data.append(i.tx_errors_carrier)
                tx_errors_collisions_data.append(i.tx_errors_collisions)
                record_dates.append(i.record_date.__format__("%d/%m/%y %H:%M:%S"))

            distributed_data.append({
                iface_name: {
                    "rx_bytes_data": rx_bytes_data,
                    "rx_packets_data": rx_packets_data,
                    "rx_errors_errors_data": rx_errors_errors_data,
                    "rx_errors_dropped_data": rx_errors_dropped_data,
                    "rx_errors_overruns_data": rx_errors_overruns_data,
                    "rx_errors_frame_data": rx_errors_frame_data,
                    "tx_bytes_data": tx_bytes_data,
                    "tx_packets_data": tx_packets_data,
                    "tx_errors_errors_data": tx_errors_errors_data,
                    "tx_errors_dropped_data": tx_errors_dropped_data,
                    "tx_errors_overruns_data": tx_errors_overruns_data,
                    "tx_errors_carrier_data": tx_errors_carrier_data,
                    "tx_errors_collisions_data": tx_errors_collisions_data,
                    "record_dates": record_dates,
                }
            })

        return {
            "distributed_data": distributed_data,
            "target_id": target_id,
            "net": True,
            "chart_num_data": ifaces_ids
        }
