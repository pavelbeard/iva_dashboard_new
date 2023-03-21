from django.urls import path
from api import views

from rest_framework_simplejwt import views as jwt_views

app_name = "api"

urlpatterns = (
    # get
    path('sslcert', views.SslCertDataAPIView.as_view()),
    path('token', jwt_views.TokenObtainPairView.as_view()),
    path('token/refresh', jwt_views.TokenRefreshView.as_view()),
    path('target_test', views.TargetHealth.as_view()),
    path('prom_targets', views.PromTargetAPIView.as_view()),
    path('prom_data', views.PromQlView.as_view()),
)

