from django import urls
from . import views


app_name = "dashboard_ivcs"

urlpatterns = [
    urls.path('main/', urls.include([
        urls.path(
            'access-log-records/<int:page>/', views.IvcsGetAccessLogRecords.as_view(), name="access_log_records"
        ),
    ]))
]