from abc import ABC

from core_logic.base import DataImporter
from dashboard import models


class DjangoORMImporter(DataImporter, ABC):
    def __init__(self, model):
        super().__init__(model)


class CPUDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, *args, **kwargs):
        labels = [f.attname for f in models.CPU._meta.fields][2:-2]
        cpu_idle_data = []
        cpu_iowait_data = []
        cpu_irq_data = []
        cpu_nice_data = []
        cpu_softirq_data = []
        cpu_steal_data = []
        cpu_sys_data = []
        cpu_user_data = []
        record_dates = []

        # TODO 24, 12, 6, 1, настраиваемый
        queryset = self.model.objects.filter(target_id=target_id).order_by("-record_date")[:50]

        for cpu_record in queryset:
            cpu_idle_data.append(cpu_record.cpu_idle)
            cpu_iowait_data.append(cpu_record.cpu_iowait)
            cpu_irq_data.append(cpu_record.cpu_irq)
            cpu_nice_data.append(cpu_record.cpu_nice)
            cpu_softirq_data.append(cpu_record.cpu_softirq)
            cpu_steal_data.append(cpu_record.cpu_steal)
            cpu_sys_data.append(cpu_record.cpu_sys)
            cpu_user_data.append(cpu_record.cpu_user)
            record_dates.append(cpu_record.record_date.__format__("%d/%m/%y %H:%M:%S"))

        return {
            "labels": labels,
            "cpu_idle_data": cpu_idle_data,
            "cpu_iowait_data": cpu_iowait_data,
            "cpu_irq_data": cpu_irq_data,
            "cpu_nice_data": cpu_nice_data,
            "cpu_softirq_data": cpu_softirq_data,
            "cpu_steal_data": cpu_steal_data,
            "cpu_sys_data": cpu_sys_data,
            "cpu_user_data": cpu_user_data,
            "record_dates": record_dates,
            "target_id": target_id,
            "cpu": True
        }


class RAMDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, *args, **kwargs):
        labels = [f.attname for f in models.RAM._meta.fields][2:-2]
        total_ram_data = []
        ram_used_data = []
        ram_free_data = []
        ram_shared_data = []
        ram_buff_cache_data = []
        ram_avail_data = []
        record_dates = []

        queryset = models.RAM.objects.filter(target_id=target_id).order_by("-record_date")[:50]

        for ram_record in queryset:
            total_ram_data.append(ram_record.total_ram)
            ram_used_data.append(ram_record.ram_used)
            ram_free_data.append(ram_record.ram_free)
            ram_shared_data.append(ram_record.ram_shared)
            ram_buff_cache_data.append(ram_record.ram_buff_cache)
            ram_avail_data.append(ram_record.ram_avail)
            record_dates.append(ram_record.record_date.__format__("%d/%m/%y %H:%M:%S"))

        return {
            "label_total_ram": labels[0],
            "remaining_labels": labels[1:],
            "total_ram_data": total_ram_data,
            "ram_used_data": ram_used_data,
            "ram_free_data": ram_free_data,
            "ram_shared_data": ram_shared_data,
            "ram_buff_cache_data": ram_buff_cache_data,
            "ram_avail_data": ram_avail_data,
            "record_dates": record_dates,
            "target_id": target_id,
            "ram": True
        }


class DiskDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, *args, **kwargs):
        filesystems_id = [
            i[0] for i in
            models.DiskSpace.objects.filter(target_id=target_id).values_list('cluster_id', 'file_system').distinct()
        ]

        filesystems_name = []
        for fs_id in filesystems_id:
            q = models.DiskSpace.objects.filter(target_id=target_id, cluster_id=fs_id).first()
            filesystems_name.append(q.file_system)

        distributed_data = []
        for fs_id, fs_name in zip(filesystems_id, filesystems_name):
            fs_size_data = []
            fs_used_data = []
            fs_avail_data = []
            record_dates = []

            for i in models.DiskSpace.objects.filter(target_id=target_id, cluster_id=fs_id).order_by("-record_date")[:50]:
                fs_size_data.append(i.fs_size)
                fs_used_data.append(i.fs_used)
                fs_avail_data.append(i.fs_avail)
                record_dates.append(i.record_date.__format__("%d/%m/%y %H:%M:%S"))

            distributed_data.append({
                fs_name: {
                    "fs_size_data": fs_size_data,
                    "fs_used_data": fs_used_data,
                    "fs_avail_data": fs_avail_data,
                    "record_dates": record_dates,
                }
            })

        return {
            "distributed_data": distributed_data,
            "target_id": target_id,
            "disk": True,
            "chart_num_data": filesystems_id,
        }


class NetDataImporter(DjangoORMImporter, ABC):
    def __init__(self, model):
        super().__init__(model)

    def import_data(self, target_id, *args, **kwargs):
        ifaces_ids = [
            i[0] for i in
            self.model.objects.filter(target_id=target_id).values_list('interface_id').distinct()
        ]

        ifaces_names = [
            self.model.objects.filter(target_id=target_id, interface_id=iface_id).first().interface
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

            for i in self.model.objects.filter(target_id=target_id, interface_id=iface_id).order_by("-record_date")[:50]:
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
