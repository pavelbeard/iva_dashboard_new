"""monitor_serv URL Configuration

The `urlpatterns` list routes URLs to views.py. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views.py
    1. Add an import:  from my_app import views.py
    2. Add a URL to urlpatterns:  path('', views.py.home, name='home')
Class-based views.py
    1. Add an import:  from other_app.views.py import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views import generic

from monitor_serv import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login-user/', views.LoginUserView.as_view(), name='login_user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('', generic.RedirectView.as_view(pattern_name="dashboard:index"), name='base'),
]
