"""monitor_serv URL Configuration

The `urlpatterns` list routes URLs to mixins.py. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function mixins.py
    1. Add an import:  from my_app import mixins.py
    2. Add a URL to urlpatterns:  path('', mixins.py.home, name='home')
Class-based mixins.py
    1. Add an import:  from other_app.mixins.py import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dashboard import views
from django.contrib import admin
from django.urls import include, path
from django.views import generic

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api/targets/', include('dashboard.urls')),
    path('api/users/', include('dashboard_users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
)
