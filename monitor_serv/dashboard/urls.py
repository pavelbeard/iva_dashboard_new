from django import urls
from django.urls import include

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
    urls.path('interval/', views.get_interval, name="interval"),
    # data access urls
    # urls.path('dal/', include([
    #     urls.path('hostnamectl/', views.ServerData.as_view(), name="dal_hostnamectl")
    # ]))
]
