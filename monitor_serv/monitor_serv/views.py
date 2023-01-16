from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate as django_auth, login as django_login, logout as django_logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views

app_version = settings.APPLICATION_VERSION


class LoginView(views.LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:dashboard"))

        return HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:index"))


class LoginUserView(views.LoginView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = django_auth(username=username, password=password)

        if user is None:
            messages.error(request, "Некорректные данные")
            return HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:index"))

        django_login(request, user)
        return HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:dashboard"))


class LogoutView(views.LogoutView):
    def get(self, request, *args, **kwargs):
        django_logout(request)
        request.user = None
        return HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:index"))
