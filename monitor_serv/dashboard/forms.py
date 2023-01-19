from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from bootstrap_modal_forms.forms import PopRequestMixin, CreateUpdateAjaxMixin


class SignupForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        models = User
        fields = 'username first_name last_name email password1 password2'.split()


class LoginForm(AuthenticationForm):
    class Meta:
        models = User
        fields = "username password".split()
