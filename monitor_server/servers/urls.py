from django.urls import path
from django.views import generic
from . import views

app_name = 'servers.html'

urlpatterns = [
    path('metrics/', generic.TemplateView.as_view(template_name="servers.html"), name="servers_index"),
    path('metrics/processes/', views.ServerProcesses.as_view(), name="servers_processes"),
]
