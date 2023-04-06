from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from .serializers import MediaServerSerializer


# from .serializers import ConferenceSessionSerializer


# Create your views here.

@api_view(['GET'])
def ping(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ConferenceData(APIView):
    def get(self, request):
        now = timezone.now()
        now_1 = timezone.now() - timedelta(minutes=1, seconds=10)

        range = now_1, now

        query = models.ConferenceSession.objects.using('ivcs') \
            .prefetch_related('parent') \
            .select_related('conferencesessionactivitystatistic') \
            .filter(conferencesessionactivitystatistic__user_count__gt=0,
                    conferencesessionactivitystatistic__collect_date__range=range)\
            .order_by('-conferencesessionactivitystatistic__collect_date')\
            .values('parent__name', 'conferencesessionactivitystatistic__user_count',
                    'parent__media_server__id')

        return Response(query, status.HTTP_200_OK)


class MediaServer(ListAPIView):
    queryset = models.MediaServer.objects.using('ivcs').all()
    serializer_class = MediaServerSerializer
