from bootstrap_modal_forms.generic import BSModalLoginView
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views, logout, login, authenticate
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . import mixins, forms


# Create your views here.

# unused
class SignupModalView(mixins.SignupLogicMixin):
    form_class = forms.SignupForm
    template_name = "auth/_signup.html"
    success_message = "Вы успешно зарегистрированы. Ожидайте подтверждения администратором!"
    success_url = reverse_lazy("dashboard:index")


# unused
class LoginModalView(BSModalLoginView):
    form_class = forms.LoginForm
    template_name = "auth/_login_modal.html"
    success_message = "Добро пожаловать!"
    success_url = reverse_lazy("dashboard:dashboard")


class RegisterView(views.FormView):
    template_name = "dashboard_users/auth/_register.html"
    form_class = forms.NewUserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request=request, template_name=self.template_name, context={
            "register_form": form,
            "app_version": settings.APP_VERSION
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация завершена. Ожидайте активации аккаунта администратором.")

            return redirect("dashboard:dashboard")

            # TODO: отобразить ошибки валидации: переписать форму

        messages.error(request, "Регистрация завершилась неудачно. Некорректная информация.")
        return render(request, self.template_name, context={"register_form": self.form_class()})


class LoginView(views.LoginView):
    template_name = "dashboard_users/auth/_login.html"
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={
            "login_form": form,
            "app_version": settings.APP_VERSION
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {username}.")
                return redirect("dashboard:dashboard")
            else:
                messages.error(request, 'Неправильный логин, либо пароль.')
        else:
            messages.error(request, 'Неправильный логин, либо пароль.')

        return render(request, self.template_name, context={
            "login_form": self.form_class(),
            "app_version": settings.APP_VERSION
        })


def logout_view(request):
    logout(request)
    messages.info(request, "Удачного мониторинга без дашборда 🤣")
    return redirect("dashboard_users:login")
