from django.db.models import Q, Count

from dashboard.models import DiskSpace, NetInterface


class Chart:
    COLOR_PALETTE = (
        "966B9D", "C98686", "F2B880", "00F4EC",
        "E7CFBC", "D1BCE3", "C49BBB", "585481",
        "19297C", "041B15", "136F63", "22AAA1",
        "4CE0D2", "84CAE7", "FFBE0B", "FB5607",
        "FF006E", "8338EC", "3A86FF", "3A86FF",
    )

    def __init__(self, model):
        self.model = model

    def create_chart_data(self, keys, target_id, filter, *args, **kwargs):
        datasets = []

        query = self.model \
            .objects \
            .filter(Q(target_id=target_id) & filter) \
            .order_by("record_date")

        for num, key in enumerate(keys):
            datasets.append({
                "label": key,
                "backgroundColor": "#" + self.COLOR_PALETTE[num],
                "borderColor": "#" + self.COLOR_PALETTE[num],
                "data": list(map(lambda i: getattr(i, key), query)),
            })
        else:
            labels = list(map(lambda i: getattr(
                i, "record_date").__format__("%d/%m/%y %H:%M:%S"), query))

        return {
            "labels": labels,
            "datasets": datasets
        }

    @staticmethod
    def set_chart_config(title, data):
        return {
            "type": "line",
            "data": data,
            "options": {
                "animation": {
                    "duration": 0
                },
                "maintainAspectRatio": False,
                "responsive": True,
                "plugins": {
                    "legend": {
                        "position": "top",
                        "labels": {
                            "color": "black",
                            "font": {
                                "size": 14,
                            }
                        }
                    },
                    "title": {
                        "color": "black",
                        "display": True,
                        "text": title,
                        "font": {
                            "size": 14
                        }
                    },
                    "scales": {
                        "yAxes": [{
                            "display": True,
                            "gridLines": {
                                "color": "#0F99CD"
                            },
                            "ticks": {
                                "max": 100,
                                "min": 0,
                                "padding": 20
                            }
                        }],
                    }
                },
            }
        }


class DiskSpaceChart(Chart):
    def __init__(self, model: DiskSpace):
        super().__init__(model)

    def create_chart_data(self, keys, target_id, filter, *args, **kwargs):
        datasets = []
        fs_name_id_array = sorted(
            [c[0] for c in self.model.objects.filter(target_id=target_id).values_list('cluster_id').distinct()]
        )

        labels = []
        query = []

        for fs_name_id in fs_name_id_array:
            for num, key in enumerate(keys):
                query = self.model\
                    .objects\
                    .filter(Q(target_id=target_id) & Q(cluster_id=fs_name_id) & filter) \
                    .order_by("record_date")
                datasets.append({
                    "label": "{" + query.filter(cluster_id=fs_name_id).first().file_system + "}=" + key,
                    "backgroundColor": "#" + self.COLOR_PALETTE[fs_name_id],
                    "borderColor": "#" + self.COLOR_PALETTE[fs_name_id],
                    "data": list(map(lambda i: getattr(i, key), query.filter(cluster_id=fs_name_id))),
                })
            else:
                labels = list(map(lambda i: getattr(
                    i, "record_date").__format__("%d/%m/%y %H:%M:%S"), query))

        return {
             "labels": labels,
             "datasets": datasets
        }


class NetInterfaceChart(Chart):
    def __init__(self, model: NetInterface):
        super().__init__(model)

    def create_chart_data(self, keys, target_id, filter, *args, **kwargs):
        datasets = []
        iface_id_array = sorted(
            [c[0] for c in self.model.objects.filter(target_id=target_id).values_list('interface_id').distinct()]
        )

        labels = []
        query = []

        for iface_id in iface_id_array:
            for num, key in enumerate(keys):
                query = self\
                    .model\
                    .objects\
                    .filter(Q(target_id=target_id) & Q(interface_id=iface_id) & filter) \
                    .order_by("record_date")
                datasets.append({
                    "label": "{" + query.filter(interface_id=iface_id).first().interface + "}=" + key,
                    "backgroundColor": "#" + self.COLOR_PALETTE[iface_id],
                    "borderColor": "#" + self.COLOR_PALETTE[iface_id],
                    "data": list(map(lambda i: getattr(i, key), query.filter(interface_id=iface_id))),
                })
            else:
                labels = list(map(lambda i: getattr(
                    i, "record_date").__format__("%d/%m/%y %H:%M:%S"), query))

        return {
            "labels": labels,
            "datasets": datasets
        }
