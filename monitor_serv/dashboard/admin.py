from common.admin import admin_url_resolver
from django.contrib import admin

from dashboard.models import Target, DashboardSettings, PromQL


# Register your models here.


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = tuple('id address port'.split())


@admin.register(PromQL)
class PromQLAdmin(admin.ModelAdmin):
    list_display = tuple('id query'.split())


@admin.register(DashboardSettings)
class BackendSettingsAdmin(admin.ModelAdmin):
    list_display = tuple('id refresh_interval'.split())
