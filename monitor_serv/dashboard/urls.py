from django import urls
from django.views import generic
from . import views


app_name = "dashboard"

urlpatterns = [
    urls.path('', generic.TemplateView.as_view(template_name="index.html")),
    urls.path('processes/', views.Processes.as_view(), name="processes"),
]
