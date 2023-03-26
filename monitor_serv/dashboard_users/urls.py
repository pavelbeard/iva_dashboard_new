from django.urls import path
from dashboard_users import views

app_name = "dashboard_users"

urlpatterns = [
    path('', views.UsersView.as_view()),
    path('authentication', views.CheckAuthentication.as_view()),
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginUserView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('update', views.UpdateUserView.as_view()),
    path('delete', views.DeleteUserView.as_view()),
    path('me', views.RetrieveUserView.as_view()),
]
