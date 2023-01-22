from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy
from . import models


# Register your models here.


# class DashboardAdmin(AdminSite):
#     site_title = gettext_lazy("")
#     pass


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = tuple('username email last_login is_superuser is_staff is_active'.split())
    list_filter = tuple('username email last_login is_superuser is_staff is_active '.split())
    actions = ['make_is_active']

    @admin.action(description="Mark this user(-s) as active", permissions=['change'])
    def make_is_active(self, modeladmin, request, queryset):
        queryset.update(is_active=True)


admin.site.site_header = "Панель администратора платформы IVA MCU Dashboard"
admin.site.index_title = "Администрирование сайта"
admin.site.site_title = "Панель администратора"
