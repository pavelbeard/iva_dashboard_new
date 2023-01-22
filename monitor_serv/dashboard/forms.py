from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from dashboard_users import models as dashboard_users_models
from . import models as dashboard_models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from bootstrap_modal_forms.forms import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import fields


class TargetForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = dashboard_models.Target
        fields = ['address', 'port', 'username', 'password', 'server_role']
