import itertools
import socket
import ssl
from collections import ChainMap

from dashboard.models import DashboardSettings


def get_ssl_cert():
    try:
        settings = DashboardSettings.objects.all().first()

        ssl_context = ssl.create_default_context()

        with socket.create_connection((settings.address_for_check_ssl, settings.port)) as sock:
            with ssl_context.wrap_socket(sock, server_hostname=settings.address_for_check_ssl) as ssock:
                issuer = dict(issuer={i[0]: i[1] for i in list(itertools.chain(*ssock.getpeercert()['issuer']))})
                valid_from = dict(validFrom=ssock.getpeercert()['notBefore'])
                valid_to = dict(validTo=ssock.getpeercert()['notAfter'])

                return dict(ChainMap(issuer, valid_from, valid_to))
    except ssl.SSLError:
        return dict(
            ChainMap(
                dict(issuer=dict(organizationName="N/A")),
                dict(validFrom=""),
                dict(validTo=""),
                dict(errors="Сертификат просрочен"))
        )
    except AttributeError as e:
        return dict(
            ChainMap(
                dict(issuer=dict(organizationName="N/A")),
                dict(validFrom=""),
                dict(validTo=""),
                dict(errors="Не найден адрес хостинга сертификата"))
        )
