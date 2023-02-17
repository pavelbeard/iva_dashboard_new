from django import urls
from django.urls import include
from . import views

app_name = "dashboard"

urlpatterns = [
    urls.path('', views.index_view, name="index"),
    urls.path('main/', include([
        urls.path('', views.dashboard_view, name="dashboard"),
        urls.path('interval/', views.get_interval, name="interval"),
        urls.path('all-metrics/', views.DataGetterFromAgent.as_view(), name="get_all_data_from_agent"),
    ])),
]
