from django import urls
from django.views import generic
from . import views


app_name = "dashboard"

urlpatterns = [
    urls.path('', generic.TemplateView.as_view(template_name="index.html"), name="index"),
    urls.path('processes/', views.Processes.as_view(), name="processes"),
    urls.path('cpu_info/', views.CPU.as_view(), name="cpu_info"),
]
