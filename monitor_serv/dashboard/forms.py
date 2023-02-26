from core_logic import pass_handler
from django import forms
from django.conf import settings

from . import models as dashboard_models

ENCRYPTION_KEY = settings.ENCRYPTION_KEY
DEBUG = settings.DEBUG


class TargetForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль сервера:")

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if DEBUG:
            print(password)
            print(ENCRYPTION_KEY)

        encrypted_password = pass_handler.encrypt_pass(password=password, encryption_key=ENCRYPTION_KEY)

        if DEBUG:
            print(encrypted_password)

        return encrypted_password

    class Meta:
        model = dashboard_models.Target
        fields = ['address', 'port', 'username', 'password', 'is_being_scan', 'scrape_command']


class ServerDataForm(forms.ModelForm):
    uuid_record = forms.UUIDField(disabled=True, label="UUID записи:")
    hostname = forms.CharField(disabled=True, label="Имя сервера:")
    os = forms.CharField(disabled=True, label="ОС Сервера:")
    kernel = forms.CharField(disabled=True, label="Ядро ОС:")
    record_date = forms.DateTimeField(disabled=True, label="Время сканирования:")
    target = forms.ModelChoiceField(disabled=True, queryset=dashboard_models.Target.objects.all(),
                                    label="Целевой хост:")

    class Meta:
        model = dashboard_models.ServerData
        fields = "__all__"


class ScrapeCommandForm(forms.ModelForm):
    pass
