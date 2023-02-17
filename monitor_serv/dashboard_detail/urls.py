from django import urls
from . import views


app_name = "dashboard_detail"

urlpatterns = [
    # urls.path('', views.index, name="index"),
    urls.path('cpu-detail/<int:target_id>/', views.cpu_view, name="cpu"),
]