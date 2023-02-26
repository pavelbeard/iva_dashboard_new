from django import urls

from . import views

app_name = "dashboard_detail"

urlpatterns = [
    urls.path('cpu-detail/<int:target_id>/', views.CPUDetailView.as_view(), name="cpu"),
    urls.path('ram-detail/<int:target_id>/', views.RAMDetailView.as_view(), name="ram"),
    urls.path('disk-detail/<int:target_id>/', views.DiskSpaceDetailView.as_view(), name="disk"),
    urls.path('net-detail/<int:target_id>/', views.NetInterfaceView.as_view(), name="net"),
]