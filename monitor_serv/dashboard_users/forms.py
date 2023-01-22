from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import fields
from . import models


class SignupForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    email = fields.EmailField(required=True)

    class Meta:
        model = models.CustomUser
        fields = 'username first_name last_name email password1 password2'.split()


class LoginForm(AuthenticationForm):
    class Meta:
        model = models.CustomUser
        fields = "username password".split()