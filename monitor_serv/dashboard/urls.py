from django import urls
from django.contrib.auth.decorators import login_required
from django.urls import include, reverse_lazy

from . import views

app_name = "dashboard"

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name="index"),
    urls.path('targets/', login_required(
        views.DashboardView.as_view(), login_url=reverse_lazy('dashboard_users:login')
    ), name="targets")
]
