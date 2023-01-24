from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth import forms
from django.forms import fields
from . import models


class SignupForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.UserCreationForm):
    email = fields.EmailField(required=True)

    class Meta:
        model = models.CustomUser
        fields = 'username first_name last_name email password1 password2'.split()


class LoginForm(forms.AuthenticationForm):
    class Meta:
        model = models.CustomUser
        fields = "username password".split()
