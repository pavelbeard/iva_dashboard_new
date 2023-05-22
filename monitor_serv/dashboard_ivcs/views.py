from datetime import timedelta, datetime

from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from .filters import AuditLogRecordFilter
from .pagination import StandardResultsSetPagination
from .serializers import MediaServerSerializer, AuditLogRecordSerializer


# Create your views here.

@api_view(['GET'])
def ping(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ConferenceData(APIView):
    def get(self, request):
        now = timezone.now()
        now_1 = timezone.now() - timedelta(minutes=1, seconds=1)

        range = now_1, now

        query = models.ConferenceSession.objects \
            .prefetch_related('parent') \
            .select_related('conferencesessionactivitystatistic') \
            .filter(conferencesessionactivitystatistic__user_count__gt=0,
                    conferencesessionactivitystatistic__collect_date__range=range) \
            .order_by('-conferencesessionactivitystatistic__collect_date') \
            .values('parent__name', 'conferencesessionactivitystatistic__user_count',
                    'parent__media_server__id')

        return Response(query, status.HTTP_200_OK)


class MediaServer(ListAPIView):
    queryset = models.MediaServer.objects.all()
    serializer_class = MediaServerSerializer


class AuditLogRecord(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = models.AuditLogRecord.objects.order_by('-date_created')
    serializer_class = AuditLogRecordSerializer
    pagination_class = StandardResultsSetPagination


class AuditLogLastEvents(GenericAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = AuditLogRecordSerializer
    queryset = models.AuditLogRecord.objects.all()

    def get(self, request):
        try:
            query = self.queryset.filter(~Q(user_ip="") & Q(severity=2)) \
                        .values('date_created', 'profile_id', 'user_ip',
                                'severity', 'record_type', 'info_json') \
                        .order_by('-date_created')[:9]
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "reason": "unexpected exception"
            }, status=status.HTTP_400_BAD_REQUEST)


class AuditLogEventsAll(APIView):
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = AuditLogRecordFilter

    def get(self, request):
        try:
            params = request.GET
            page_size = params.get('page_size', 25)

            self.pagination_class.page_size = int(page_size)
            queryset = models.AuditLogRecord.objects.order_by('-date_created')

            paginator = self.pagination_class()

            filtered_queryset = self.filterset_class(request.GET, queryset).qs
            page = paginator.paginate_queryset(filtered_queryset, request)
            serializer = AuditLogRecordSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)

            return Response(paginated_response.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "status": "error",
                "reason": "unexpected exception"
            }, status=status.HTTP_400_BAD_REQUEST)


class PlannedConference(APIView):
    permission_classes = (AllowAny, )
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = None

    def get(self, request):
        try:
            params = request.GET
            page_size = params.get('page_size', 25)

            self.pagination_class.page_size = int(page_size)
            query = models.Conference.objects\
                .select_related('owner')\
                .filter(~Q(conference_number=None))

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(
                query.values('name', 'owner__name', 'start_date', 'conference_number'), request
            )
            paginated_response = paginator.get_paginated_response(page)

            # запрос: по каждому мероприятию нужно узнать количество юзеров в данный момент времени
            now = timezone.now()
            now_1 = timezone.now() - timedelta(minutes=1, seconds=1)

            return Response(paginated_response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "unexpected exception"
            }, status=status.HTTP_400_BAD_REQUEST)
