from dashboard_users import views
from django import urls
from django.urls import include

app_name = "dashboard_users"

urlpatterns = [
    urls.path('', include([
        urls.path('register/', views.RegisterView.as_view(), name='register'),
        urls.path('login/', views.UserLoginView.as_view(), name='login'),
        urls.path('logout/', views.logout_view, name='logout'),
    ])),
]
