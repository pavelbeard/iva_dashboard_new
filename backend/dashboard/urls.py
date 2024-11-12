from django.contrib.auth.decorators import login_required
from django.urls import include, reverse_lazy, path

from . import views

app_name = "dashboard"

urlpatterns = (
    path('all', views.TargetAPIView.as_view()),
    path('settings', views.BackendSettingsAPIView.as_view()),
)
