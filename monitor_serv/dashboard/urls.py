from django import urls
from django.urls import include
from . import views

app_name = "dashboard"

urlpatterns = [
    urls.path('', views.index_view, name="index"),
    urls.path('main/', include([
        urls.path('', views.dashboard_view, name="dashboard"),
        # urls.path('hostnamectl/', views.ServerData.as_view(), name="hostnamectl"),
        # urls.path('cputopanalysis/', views.CPUTop.as_view(), name="cpu_top_info"),
        # urls.path('ramanalysis/', views.RAM.as_view(), name="ram_info"),
        # urls.path('filesysanalysisparts/', views.DiskSpace.as_view(), name="disk_info"),
        # urls.path('execanalysis/', views.Processes.as_view(), name="processes"),
        # urls.path('netanalysis/', views.Net.as_view(), name="net_info"),
        # urls.path('uptime/', views.Uptime.as_view(), name="uptime"),
        urls.path('interval/', views.get_interval, name="interval"),
        urls.path('all-metrics/', views.DataGetterFromAgent.as_view(), name="get_all_data_from_agent"),
    ])),
]
