from django import urls
from django.urls import include
from . import views

app_name = "dashboard"

urlpatterns = [
    urls.path('', views.index_view, name="index"),
    urls.path('main/', include([
        urls.path('', views.dashboard_view, name="dashboard"),
        urls.path('hostnamectl/', views.ServerData.as_view(), name="hostnamectl"),
        urls.path('cpu-top-info/', views.CPUTop.as_view(), name="cpu_top_info"),
        urls.path('ram-info/', views.RAM.as_view(), name="ram_info"),
        urls.path('disk-info/', views.DiskSpace.as_view(), name="disk_info"),
        urls.path('processes/', views.Processes.as_view(), name="processes"),
        urls.path('net-info/', views.Net.as_view(), name="net_info"),
        urls.path('uptime/', views.Uptime.as_view(), name="uptime"),
        urls.path('interval/', views.get_interval, name="interval"),
    ])),
]
