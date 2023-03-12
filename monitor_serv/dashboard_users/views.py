from common.mixins import AppVersionMixin, ErrorMessageMixin
from dashboard_users.forms import LoginForm, NewUserForm
from dashboard_users.models import CustomUser
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.
class RegisterView(SuccessMessageMixin, ErrorMessageMixin, AppVersionMixin, CreateView):
    model = CustomUser
    form_class = NewUserForm
    template_name = "dashboard_users/auth/_register.html"
    success_message = "Регистрация завершена. Ожидайте активации аккаунта администратором."
    success_url = reverse_lazy("dashboard_users:login")
    error_message = "Регистрация завершилась неудачно. Некорректная информация."


class UserLoginView(AppVersionMixin, LoginView):
    form_class = LoginForm
    template_name = "dashboard_users/auth/_login.html"
    success_url = reverse_lazy("dashboard:targets")

    def form_valid(self, form):
        messages.info(self.request, f"Вы вошли как {form.cleaned_data.get('username')}.")
        return super().form_valid(form)

    def form_invalid(self, form):
        try:
            user = CustomUser.objects.get(username=form.cleaned_data.get('username').lower())

            if user is None:
                raise CustomUser.DoesNotExist
            elif not user.is_active:
                messages.error(self.request, 'Ваш аккаунт еще не активирован.')
            elif not check_password(form.cleaned_data.get('password'), user.password):
                messages.error(self.request, 'Неправильный логин, либо пароль.')
        except CustomUser.DoesNotExist:
            messages.error(self.request, 'Пользователь не найден.')
        finally:
            return super().form_invalid(form)


def logout_view(request):
    logout(request)
    messages.info(request, "Удачного мониторинга без дашборда 🤣")
    return redirect("dashboard:index")
