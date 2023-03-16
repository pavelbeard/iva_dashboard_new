import json
from abc import ABC, abstractmethod
from http import HTTPStatus

import requests
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from api.logic import CpuDataHandler, RamDataHandler, FilesystemDataHandler, get_ssl_cert, NetworkDataHandler
from api.mixins import PromQueryMixin
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
        url = f"http://{prom_target_address}/api/v1/targets?state=any"
        response = requests.get(url)

        if response.status_code > 400:
            return JsonResponse(data={"message": "error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        json_response = response.json()
        return JsonResponse(data=json_response, safe=False, status=HTTPStatus.OK)


class CpuDataAPIView(PromQueryMixin, BaseDataView, APIView):
    data_handler_class = CpuDataHandler

    def get(self, request, prom_target_address):
        context = json.dumps(self.get_context_data(request, prom_target_address))
        return JsonResponse(data=context, status=HTTPStatus.OK, safe=False)


class RamDataAPIView(PromQueryMixin, BaseDataView, APIView):
    data_handler_class = RamDataHandler

    def get(self, request, prom_target_address):
        context = json.dumps(self.get_context_data(request, prom_target_address))
        return JsonResponse(data=context, status=HTTPStatus.OK, safe=False)


class FilespaceDataAPIView(PromQueryMixin, BaseDataView, APIView):
    data_handler_class = FilesystemDataHandler

    def get(self, request, prom_target_address):
        context = json.dumps(self.get_context_data(request, prom_target_address))
        return JsonResponse(data=context, status=HTTPStatus.OK, safe=False)


class AppsDataAPIView(PromQueryMixin,  BaseDataView, APIView):
    def get(self, *args, **kwargs):
        pass


class NetworkDataAPIView(PromQueryMixin, BaseDataView, APIView):
    data_handler_class = NetworkDataHandler

    def get(self, request, prom_target_address):
        # context = json.dumps(self.get_context_data(request, prom_target_address))
        context = requests.get(f"http://{prom_target_address}/api/v1/query?query={request.GET['query']}")
        return JsonResponse(data=context.json(), status=HTTPStatus.OK, safe=False)


class SslCerDataAPIView(TemplateView, APIView):
    def get(self, request, **kwargs):
        try:
            ssl_data = get_ssl_cert()
            return JsonResponse(data=ssl_data, status=HTTPStatus.OK, safe=False)
        except ConnectionError:
            return JsonResponse(data={"error": "no connection with server"},
                                status=HTTPStatus.NOT_ACCEPTABLE, safe=False)
        except AttributeError:
            return JsonResponse(data={"error": "unexpected error"},
                                status=HTTPStatus.INTERNAL_SERVER_ERROR, safe=False)


