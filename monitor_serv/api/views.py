import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.logic import get_ssl_cert


# Create your views here.


class PromTargetView(APIView):
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
