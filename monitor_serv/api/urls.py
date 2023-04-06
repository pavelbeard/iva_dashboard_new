from django.urls import path
from api import views

from rest_framework_simplejwt import views as jwt_views

app_name = "api"

urlpatterns = (
    path('sslcert', views.SslCertDataView.as_view()),
    path('target_test', views.TargetHealth.as_view()),
    path('prom_targets', views.PromTargetView.as_view()),
    path('prom_data', views.PromQlView.as_view()),
    path('csrf_cookie', views.GetCSRF.as_view()),
    path('app_version', views.get_backend_version),

    path('services_status/<int:server_id>', views.ServicesStatus.as_view()),
    path('ping', views.ping),
)

