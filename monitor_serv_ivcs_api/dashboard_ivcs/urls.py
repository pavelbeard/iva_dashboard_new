from django.urls import path

from . import views

app_name = "dashboard_ivcs"

urlpatterns = (
    path('conference_data', views.ConferenceData.as_view()),
    path('media_servers', views.MediaServer.as_view()),
    path('ping', views.ping),
)
