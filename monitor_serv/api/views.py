import json

import requests
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.logic import get_ssl_cert
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
    def create_url(prom_target, query):
        return f'http://{prom_target}/api/v1/{query}'

    def get(self, request):
        query = request.GET.get('query')
        host = request.GET.get('host')
        query_range = request.GET.get('query_range')
        start = request.GET.get('start')
        end = request.GET.get('end')
        step = request.GET.get('step')

        boolean_true_list = ['True', 'true']

        query_type = "query_range?query" if query_range in boolean_true_list else "query?query"

        completed_query = f"{query_type}={query}"

        if start:
            completed_query += f"&{start}"
        if end:
            completed_query += f"&{end}"
        if step:
            completed_query += f"&{step}"

        try:
            context = requests.get(self.create_url(host, completed_query))
            return Response(data=context.json(), status=status.HTTP_200_OK)
        except requests.exceptions.ConnectionError:
            return Response(data={"status": f"no connection with {host}"})


class SslCertDataView(APIView):
    def get(self, request, **kwargs):
        try:
            ssl_data = get_ssl_cert()
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
