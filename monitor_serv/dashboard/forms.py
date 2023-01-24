from django import forms
from django.conf import settings
from logic import pass_handler
from . import models as dashboard_models


ENCRYPTION_KEY = settings.ENCRYPTION_KEY


class TargetForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль сервера:")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        encrypted_password = pass_handler.encrypt_pass(password=password, encryption_key=ENCRYPTION_KEY)

        return encrypted_password

    class Meta:
        model = dashboard_models.Target
        fields = ['address', 'port', 'username', 'password', 'server_role']
