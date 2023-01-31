from django.contrib import admin
from dashboard_users import models as dashboard_users_models
from . import models as dashboard_models
from . import forms


# Register your models here.

@admin.register(dashboard_models.Target)
class TargetAdmin(admin.ModelAdmin):
    form = forms.TargetForm
