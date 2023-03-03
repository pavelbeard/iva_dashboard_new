import math


def singleton(cls_):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls_ not in instances:
            instances[cls_] = cls_(*args, **kwargs)
        return instances[cls_]

    return wrapper


def row_2_dict(row) -> dict:
    """
    Превращает модель SQLAlchemy в словарь
    :param row: модель SQLAlchemy
    :return: dict
    """
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d


class DigitalDataConverters:
    @staticmethod
    def convert_metric_to_bytes(amount: str) -> float:
        """
        Конвертирует единицы измерения информации в метрической системе в байты.\n
        :param amount: Количество тера-, гига-, мега-, кило- и просто байтов
        :return: float
        """
        if amount.__contains__("T"):
            return float(amount[:-1]) * 1000 ** 4
        if amount.__contains__("G"):
            return float(amount[:-1]) * 1000 ** 3
        elif amount.__contains__("M"):
            return float(amount[:-1]) * 1000 ** 2
        elif amount.__contains__("K"):
            return float(amount[:-1]) * 1000
        elif amount == "0":
            return float(amount)
        else:
            return float(amount[:-1])

    @staticmethod
    def convert_bytes_to_metric(amount) -> str:
        """
        Конвертирует байты в международные единицы измерения информации в метрической системе.\n
        :param amount: Количество байтов
        :return: str
        """
        # try:
        #     amount_of_bytes = float(amount)
        #     if 0.0 <= amount_of_bytes < 1000.0:
        #         return f"{amount_of_bytes:10.2f}B".strip()
        #     elif 1000.0 <= amount_of_bytes < 1_000_000.0:
        #         return f"{amount_of_bytes / 1000:10.2f}KB".strip()
        #     elif 1_000_000.0 <= amount_of_bytes < 1_000_000_000.0:
        #         return f"{amount_of_bytes / 1000 ** 2:10.2f}MB".strip()
        #     elif 1_000_000_000.0 <= amount_of_bytes <= 1_000_000_000_000.0:
        #         return f"{amount_of_bytes / 1000 ** 3:10.2f}GB".strip()
        #     elif 1_000_000_000_000.0 <= amount_of_bytes <= 1_000_000_000_000_000.0:
        #         return f"{amount_of_bytes / 1000 ** 4:10.2f}TB".strip()
        #     else:
        #         return str(int(amount_of_bytes))
        # except ValueError:
        #     return '0'
        size_bytes = int(amount)

        if size_bytes == 0:
            return "0B"

        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", )
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)

        return f"{s}{size_name[i]}"

    @staticmethod
    def from_cidr_to_prefixlen(ipaddr: str, netmask: str) -> str:
        splitted_nm = [
            int(i) for i in "".join(["{0:b}".format(int(octet)) for octet in netmask.split(".")]).replace("0", "")
        ]
        prefixlen = sum(splitted_nm)
        return f"{ipaddr}/{prefixlen}"
