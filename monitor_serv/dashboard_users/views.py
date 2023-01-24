from bootstrap_modal_forms.generic import BSModalLoginView
from django import http
from django.contrib.auth import views, logout
from django.urls import reverse_lazy
from . import mixins, forms


# Create your views here.


class SignupView(mixins.SignupLogicMixin):
    form_class = forms.SignupForm
    template_name = "auth/_signup.html"
    success_message = "Вы успешно зарегистрированы. Ожидайте подтверждения администратором!"
    success_url = reverse_lazy("dashboard:index")


class LoginView(BSModalLoginView):
    form_class = forms.LoginForm
    template_name = "auth/_login.html"
    success_message = "Добро пожаловать!"
    success_url = reverse_lazy("dashboard:dashboard")


class LogoutView(views.LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        request.user = None
        return http.HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:index"))
