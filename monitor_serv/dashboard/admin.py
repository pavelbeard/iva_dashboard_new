from common.admin import admin_url_resolver
from django.contrib import admin

from dashboard.models import Target, DashboardSettings


# Register your models here.


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = tuple('id address port'.split())


@admin.register(DashboardSettings)
class BackendSettingsAdmin(admin.ModelAdmin):
    list_display = tuple('id address_for_check_ssl port'.split())
