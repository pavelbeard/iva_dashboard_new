from django.urls import path
from dashboard_users import views

app_name = "dashboard_users"

urlpatterns = [
    path('', views.UserAPIView.as_view()),
    path('register', views.RegisterAPIView.as_view()),
    path('login', views.LoginUserAPIView.as_view()),
    path('me', views.RetrieveUserAPIView.as_view()),
]
