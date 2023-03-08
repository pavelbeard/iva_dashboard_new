from rest_framework.generics import ListCreateAPIView

from api.serializers import TargetSerializer, CpuDataSerializer
from dashboard.models import Target, CPU


# Create your views here.

class TargetView(ListCreateAPIView):
    queryset = Target.objects.filter(is_being_scan=True)
    serializer_class = TargetSerializer
    # permission_classes = (IsAuthenticated, )


class CpuView(ListCreateAPIView):
    queryset = CPU.objects.filter(target_id=3)
    serializer_class = CpuDataSerializer
