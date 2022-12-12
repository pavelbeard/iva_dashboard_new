from django.urls import path
from django.views import generic
from . import views

app_name = 'servers.html'

urlpatterns = [
    path('', generic.TemplateView.as_view(template_name="servers.html"), name="servers_index"),
    path('metrics/', views.ServersMetricsLogicView.as_view(), name="servers_metrics"),
]
