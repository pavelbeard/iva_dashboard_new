from django.urls import path

from . import views

app_name = 'servers'

urlpatterns = [
    # path('', views.ServerServicesStates.as_view(), name="index")
    path('', views.ServerSystemctlStatus.as_view(), name="index")
]
