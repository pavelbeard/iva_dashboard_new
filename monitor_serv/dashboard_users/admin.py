from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = tuple('username email last_login is_superuser is_staff is_active'.split())
    list_filter = tuple('username email last_login is_superuser is_staff is_active '.split())
    actions = ['make_is_active']

    @admin.action(description="Mark this user(-s) as active", permissions=['change'])
    def make_is_active(self, modeladmin, request, queryset):
        queryset.update(is_active=True)