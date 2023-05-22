from django.urls import path

from . import views

app_name = "dashboard_ivcs"

urlpatterns = (
    path('conference_data', views.ConferenceData.as_view()),
    path('media_servers', views.MediaServer.as_view()),
    path('audit_log', views.AuditLogRecord.as_view()),
    path('audit_log_last_events', views.AuditLogLastEvents.as_view()),
    path('audit_log_events', views.AuditLogEventsAll.as_view()),
    path('planned_conferences', views.PlannedConference.as_view()),
    path('ping', views.ping),
)
