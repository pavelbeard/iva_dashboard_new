from django.urls import path

from api import views

app_name = "api"

urlpatterns = (
    path('targets/', views.TargetAPIView.as_view(),  name="targets"),
    path('queries/', views.PromQlAPIView.as_view(),  name="queries"),
    path('settings/', views.BackendSettingsAPIView.as_view(),  name="settings"),
)

