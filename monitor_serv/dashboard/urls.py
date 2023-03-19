from django.contrib.auth.decorators import login_required
from django.urls import include, reverse_lazy, path

from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('targets/', login_required(
        views.DashboardView.as_view(),
        login_url=reverse_lazy('dashboard_users:login')
    ), name="targets"),
    path('targets/detail/', login_required(
        views.DashboardView.as_view(),
        login_url=reverse_lazy('dashboard_users:login')
    ), name="target_detail")
]
