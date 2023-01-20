from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from . import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from bootstrap_modal_forms.forms import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import fields


class SignupForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    email = fields.EmailField(required=True)

    class Meta:
        model = models.CustomUser
        fields = 'username first_name last_name email password1 password2'.split()


class LoginForm(AuthenticationForm):
    class Meta:
        model = models.CustomUser
        fields = "username password".split()


class TargetForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.Target
        fields = ['address', 'port', 'username', 'password', 'server_role']
