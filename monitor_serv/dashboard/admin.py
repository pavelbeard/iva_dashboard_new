from django.contrib import admin
from django import forms
from . import models


class TargetForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.Target
        fields = ['address', 'port', 'username', 'password', 'server_role']


# Register your models here.

@admin.register(models.Target)
class TargetAdmin(admin.ModelAdmin):
    form = TargetForm


@admin.register(models.Server)
class ServerAdmin(admin.ModelAdmin):
    pass
