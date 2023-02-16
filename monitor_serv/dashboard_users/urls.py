from django import urls
from django.urls import include
from . import views

app_name = "dashboard_users"

urlpatterns = [
    urls.path('', include([
        urls.path('register/', views.RegisterView.as_view(), name='register'),
        urls.path('login/', views.LoginView.as_view(), name='login'),
        urls.path('logout/', views.logout_view, name='logout'),
    ])),
]
