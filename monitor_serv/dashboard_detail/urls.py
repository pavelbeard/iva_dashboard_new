from django import urls
from . import views


app_name = "dashboard_detail"

urlpatterns = [
    urls.path('', views.index, name="index"),
    urls.path('net-info-detail/', views.NetDetail, name="index"),
]