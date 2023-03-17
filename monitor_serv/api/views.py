from abc import abstractmethod
from http import HTTPStatus

import requests
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from api.logic import get_ssl_cert
from api.serializers import TargetSerializer, PromQLSerializer, BackendSettingsSerializer
from common.mixins import EmptyQueryCheckMixin
from dashboard.models import Target, PromQL, DashboardSettings


# Create your views here.

class BaseDataView(TemplateView):
    data_handler_class = None

    @abstractmethod
    def get(self, *args, **kwargs):
        pass


class TargetAPIView(EmptyQueryCheckMixin, ListAPIView):
    model = Target
    serializer_class = TargetSerializer


class PromQlAPIView(EmptyQueryCheckMixin, ListAPIView):
    model = PromQL
    serializer_class = PromQLSerializer


class BackendSettingsAPIView(EmptyQueryCheckMixin, ListAPIView):
    model = DashboardSettings
    serializer_class = BackendSettingsSerializer


class PromTargetAPIView(APIView):
    def get(self, request, prom_target_address):
        try:
            url = f"http://{prom_target_address}/api/v1/targets?state=any"
            response = requests.get(url)
            json_response = response.json()
            return JsonResponse(data=json_response, safe=False, status=HTTPStatus.OK)
        except requests.exceptions.ConnectionError:
            return JsonResponse(data={"status": f"no connection with {prom_target_address}"}, status=HTTPStatus.OK)


def ping_prom_target(request, prom_target_address):
    try:
        url = f"http://{prom_target_address}"
        response = requests.get(url)
        if not response.status_code > 400:
            return JsonResponse(data={"status": "success"})
    except requests.exceptions.ConnectionError:
        return JsonResponse(data={"status": f"no connection with {prom_target_address}"}, status=HTTPStatus.OK)


class PromQlView(BaseDataView, APIView):
    @staticmethod
    def create_url(prom_target, query):
        return f'http://{prom_target}/api/v1/{query}'

    def get(self, request, prom_target_address):
        try:
            context = requests.get(self.create_url(prom_target_address, request.GET['query']))
            return JsonResponse(data=context.json(), status=HTTPStatus.OK, safe=False)
        except requests.exceptions.ConnectionError:
            return JsonResponse(
                data={"status": f"no connection with {prom_target_address}"},
                status=HTTPStatus.OK)


class SslCerDataAPIView(TemplateView, APIView):
    def get(self, request, **kwargs):
        try:
            ssl_data = get_ssl_cert()
            return JsonResponse(data=ssl_data, status=HTTPStatus.OK, safe=False)
        except ConnectionError:
            return JsonResponse(data={"status": "no connection with server"},
                                status=HTTPStatus.NOT_ACCEPTABLE, safe=False)
        except AttributeError:
            return JsonResponse(data={"status": "unexpected error"},
                                status=HTTPStatus.INTERNAL_SERVER_ERROR, safe=False)
