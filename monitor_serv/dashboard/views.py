import asyncio

from asgiref.sync import sync_to_async
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Target, DashboardSettings
from .serializers import TargetSerializer, BackendSettingsSerializer


# Create your views here.

class TargetAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TargetSerializer

    def get_queryset(self):
        queryset = Target.objects.filter(is_being_scan=True)
        return queryset

    def get(self, request, **kwargs):
        query = self.get_queryset()
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BackendSettingsAPIView(ListAPIView):
    queryset = DashboardSettings.objects.all()
    serializer_class = BackendSettingsSerializer

