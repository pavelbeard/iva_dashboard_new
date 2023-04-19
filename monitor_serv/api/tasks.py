import socket
import ssl
from datetime import datetime, timedelta

import OpenSSL
import requests
from celery import shared_task

from dashboard.models import DashboardSettings


@shared_task
def request_for_prom_data(url):
    response = requests.get(url)
    return response.json()


def check_ssl_cert():
    issuer = None
    valid_from = None
    valid_to = None
    try:
        settings = DashboardSettings.objects.all().first()
        host = settings.address_for_check_ssl
        port = settings.port

        context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        conn = OpenSSL.SSL.Connection(context, socket.create_connection((host, port)))
        conn.set_connect_state()
        conn.do_handshake()

        # Получение и проверка сертификата сервера
        cert = conn.get_peer_certificate()
        if not cert:
            raise ssl.SSLError("Не найден сертификат сервера")

        dateBefore = cert.get_notBefore().decode('utf-8').replace('Z', '')
        dateAfter = cert.get_notAfter().decode('utf-8').replace('Z', '')
        yyyy_before, yyyy_after = dateBefore[:4], dateAfter[:4]
        mm_before, mm_after = dateBefore[4:6], dateAfter[4:6]
        dd_before, dd_after = dateBefore[6:8], dateAfter[6:8]
        HH_before, HH_after = dateBefore[8:10], dateAfter[8:10]
        MM_before, MM_after = dateBefore[10:12], dateAfter[10:12]
        ss_before, ss_after = dateBefore[12:14], dateAfter[12:14]
        issuer = cert.get_issuer().get_components()[1][1].decode('utf-8')
        valid_from = datetime.fromisoformat(
            f"{yyyy_before}-{mm_before}-{dd_before} {HH_before}:{MM_before}:{ss_before}"
        )
        valid_to = datetime.fromisoformat(
            f"{yyyy_after}-{mm_after}-{dd_after} {HH_after}:{MM_after}:{ss_after}"
        )
        conn.close()

        date_belongs = valid_from <= datetime.now() <= valid_to

        if not date_belongs:
            raise ssl.SSLError("Сертификат просрочен")

        date_range = [(valid_to - timedelta(days=d)).date() for d in range((valid_to - valid_from).days)]

        days_remaining = date_range.index(datetime.now().date())

        return {
            "issuer": issuer,
            "validFrom": valid_from,
            "validTo": valid_to,
            "daysRemaining": days_remaining
        }

    except AttributeError as e:
        return {
            "issuer": issuer,
            "validFrom": valid_from,
            "validTo": valid_to,
            "errors": "Сертификат не найден",
            "daysRemaining": -1
        }
    except ssl.SSLError as e:
        return {
            "issuer": issuer,
            "validFrom": valid_from,
            "validTo": valid_to,
            "errors": e.args[0],
            "daysRemaining": 0
        }
    except Exception as e:
        return {
            "issuer": issuer,
            "validFrom": valid_from,
            "validTo": valid_to,
            "errors": "Неизвестная ошибка.",
            "daysRemaining": -1
        }
