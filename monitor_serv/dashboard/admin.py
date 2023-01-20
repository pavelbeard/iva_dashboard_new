from django.contrib import admin
from django import forms
from . import models
from . import forms


# Register your models here.

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Server)
class ServerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Target)
class TargetAdmin(admin.ModelAdmin):
    form = forms.TargetForm
