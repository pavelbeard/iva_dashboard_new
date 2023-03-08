from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path('targets/', views.TargetView.as_view(), name="targets"),
]
