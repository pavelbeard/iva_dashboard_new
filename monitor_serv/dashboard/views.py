from rest_framework.generics import ListAPIView

from .models import Target, DashboardSettings
from .serializers import TargetSerializer, BackendSettingsSerializer


# Create your views here.

class TargetAPIView(ListAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class BackendSettingsAPIView(ListAPIView):
    queryset = DashboardSettings.objects.all()
    serializer_class = BackendSettingsSerializer
