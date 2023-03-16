from django.urls import path

from api import views

app_name = "api"

urlpatterns = (
    path('targets/', views.TargetAPIView.as_view(),  name="targets"),
    path('queries/', views.PromQlAPIView.as_view(),  name="queries"),
    path('settings/', views.BackendSettingsAPIView.as_view(),  name="settings"),
    path('ssl_test/', views.SslCerDataAPIView.as_view(),  name="ssl_test"),
    path('prom_targets/<str:prom_target_address>', views.PromTargetAPIView.as_view(),  name="prom_targets"),
    path('prom_data/<str:prom_target_address>/', views.PromQlView.as_view(), name="prom_data"),
    # path('ram_data/<str:prom_target_address>/', views.RamDataAPIView.as_view(), name="ram_data"),
    # path('filesystem_data/<str:prom_target_address>/', views.FilespaceDataAPIView.as_view(), name="filesystem_data"),
    # path('apps_data/<str:prom_target_address>/', views.AppsDataAPIView.as_view(), name="apps_data"),
    # path('net_data/<str:prom_target_address>/', views.NetworkDataAPIView.as_view(), name="net_data"),
)

