from django import urls
from django.contrib.auth.decorators import login_required
from django.urls import include, reverse_lazy

from . import views

app_name = "dashboard"

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name="index"),
    urls.path('main/', include([
        urls.path('', login_required(views.DashboardView.as_view(),
                                     login_url=reverse_lazy('dashboard_users:login')), name="dashboard"),
        urls.path('interval/', views.IntervalView.as_view(), name="interval"),
        urls.path('all-metrics/', views.DataGetterFromAgent.as_view(), name="get_all_data_from_agent"),
        urls.path('check-agent-health/', views.CheckAgentHealth.as_view(), name="check_agent_health"),
    ])),
]
