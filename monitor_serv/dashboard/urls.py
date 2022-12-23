from django import urls
from django.views import generic
from . import views


app_name = "dashboard"

urlpatterns = [
    urls.path('', views.index_view, name="index"),
    urls.path('processes/', views.Processes.as_view(), name="processes"),
    urls.path('cpu-info/', views.CPU.as_view(), name="cpu_info"),
    urls.path('ram-info/', views.RAM.as_view(), name="ram_info"),
    urls.path('disk-info/', views.DiskSpace.as_view(), name="disk_info"),
    urls.path('net-info/', views.Net.as_view(), name="net_info"),
    urls.path('uptime/', views.Uptime.as_view(), name="uptime"),
]
