from django.shortcuts import render
from rest_framework.generics import ListAPIView

from common.mixins import EmptyQueryCheckMixin
from dashboard.models import Target, PromQL, BackendSettings
from api.serializers import TargetSerializer, PromQLSerializer, BackendSettingsSerializer


# Create your views here.

class TargetAPIView(EmptyQueryCheckMixin, ListAPIView):
    model = Target
    serializer_class = TargetSerializer


class PromQlAPIView(EmptyQueryCheckMixin, ListAPIView):
    model = PromQL
    serializer_class = PromQLSerializer


class BackendSettingsAPIView(EmptyQueryCheckMixin, ListAPIView):
    model = BackendSettings
    serializer_class = BackendSettingsSerializer
