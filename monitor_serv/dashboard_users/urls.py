from django import urls
from django.urls import include
from . import views

app_name = "dashboard_users"

urlpatterns = [
    urls.path('', include([
        urls.path('signup/', views.SignupView.as_view(), name='signup'),
        urls.path('login/', views.LoginView.as_view(), name='login'),
        urls.path('logout/', views.LogoutView.as_view(), name='logout'),
    ])),
]
