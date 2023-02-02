from django.contrib import admin
from dashboard_users import models as dashboard_users_models
from . import models as dashboard_models
from . import forms


# Register your models here.

@admin.register(dashboard_models.Target)
class TargetAdmin(admin.ModelAdmin):
    form = forms.TargetForm


@admin.register(dashboard_models.ServerData)
class ServerDataAdmin(admin.ModelAdmin):
    form = forms.ServerDataForm


@admin.register(dashboard_models.CPU)
class CPUAdmin(admin.ModelAdmin):
    pass


@admin.register(dashboard_models.RAM)
class RAMAdmin(admin.ModelAdmin):
    pass


@admin.register(dashboard_models.DiskSpace)
class DiskSpaceAdmin(admin.ModelAdmin):
    pass


@admin.register(dashboard_models.NetInterface)
class NetInterfaceAdmin(admin.ModelAdmin):
    pass


@admin.register(dashboard_models.DashboardSettings)
class DashboardSettingsAdmin(admin.ModelAdmin):
    pass
