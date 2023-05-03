from urllib.parse import quote
from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.tasks import check_ssl_cert, request_for_prom_data
from common.pass_handler import decrypt_pass

from common.ssh import ssh_scraper
from common.parsers import service_status_all_parser

from dashboard.models import Target, BackendVersion


# Create your views here.

class Ping(APIView):
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class PromTargetView(APIView):
    def get(self, request):
        host = request.GET.get('host')
        try:
            url = f"http://{host}/api/v1/targets?state=any"
            response = requests.get(url)
            return Response(data=response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.ConnectionError:
            return Response(
                data={"status": f"no connection with {host}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class TargetHealth(APIView):
    def get(self, request):
        host = request.GET.get('host')

        try:
            url = f"http://{host}"
            response = requests.get(url)
            if not response.status_code > 400:
                return Response(data={"status": "success"}, status=status.HTTP_200_OK)
        except requests.exceptions.ConnectionError:
            return Response(
                data={"status": f"no connection with {host}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class PromQlView(APIView):
    @staticmethod
    def normalize_date(date_time: str):
        date_time = datetime.fromisoformat(date_time)
        date_time = date_time - timedelta(hours=3)
        return date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def create_url(prom_target, query):
        return f'http://{prom_target}/api/v1/{query}'

    def get(self, request):
        params = request.GET

        query = params.get('query')
        host = params.get('host')
        query_range = params.get('query_range')
        start = params.get('start')
        end = params.get('end')
        step = params.get('step')

        boolean_true_tuple = ('True', 'true')

        query_type = "query_range?query" if query_range in boolean_true_tuple else "query?query"

        completed_query = f"{query_type}={quote(query)}"

        if start:
            completed_query += f"&start={self.normalize_date(start)}"
        if end:
            completed_query += f"&end={self.normalize_date(end)}"
        if step:
            completed_query += f"&step={step}"

        try:
            url = self.create_url(host, completed_query)
            response = request_for_prom_data.delay(url)
            context = response.get()
            return Response(data=context, status=status.HTTP_200_OK)
        except requests.exceptions.ConnectionError:
            return Response(data={"status": f"no connection with {host}"})
        except TimeoutError:
            return Response({"status": "timeout error"})


class SslCertDataView(APIView):
    def get(self, request, **kwargs):
        try:
            ssl_data = check_ssl_cert()
            return Response(data=ssl_data, status=status.HTTP_200_OK)
        except ConnectionError:
            return Response(data={"status": "no connection with server"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except AttributeError:
            return Response(data={"status": "unexpected error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRF(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({"status": "success csrf set"}, status=status.HTTP_200_OK)


class ServicesStatus(APIView):
    def get(self, request, server_id):
        try:
            target = Target.objects.get(id=server_id)
            username = target.username
            password = decrypt_pass(settings.ENCRYPTION_KEY, target.password)
            host = target.address
            port = target.port_ssh

            raw_data = ssh_scraper("/usr/sbin/service --status-all",
                                   username=username, password=password,
                                   host=host, port=port)
            if not raw_data:
                return Response({"error": "no data"}, status.HTTP_400_BAD_REQUEST)

            result = service_status_all_parser(data=raw_data, instance=f"{host}:{port}")

            data = {"resultType": "vector"}
            data.update(result)

            return Response({"status": "success", "data": data}, status.HTTP_200_OK)
        except Target.DoesNotExist:
            return Response({"error": "target not found"}, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_backend_version(request):
    try:
        version = BackendVersion.objects.get(id=1)
        return Response({"success": version.version})
    except BackendVersion.DoesNotExist:
        return Response({"error": "version not exists"})
