from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Target)
class TargetAdmin(admin.ModelAdmin):
    fields = ['address', 'port', 'username', 'password']
