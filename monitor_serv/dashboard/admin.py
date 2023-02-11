from typing import List

from django.contrib import admin
from django.db.models import QuerySet

from core_logic.extentions import admin_url_resolver
from . import forms
from . import models


# Register your models here.
@admin.register(models.ScrapeCommand)
class ScrapeCommandAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Target)
class TargetAdmin(admin.ModelAdmin):
    form = forms.TargetForm
    list_display = tuple('id address port is_being_scan get_monitoring_commands'.split())
    actions = tuple('set_is_being_scan_false set_is_being_scan_true switch_is_being_true'.split())

    @admin.action(description="Пометить сервер(-а) как недоступного(-ые) для мониторинга.", permissions=['change'])
    def set_is_being_scan_false(self, request, queryset):
        queryset.update(is_being_scan=False)

    @admin.action(description="Пометить сервер(-а) как доступного(-ые) для мониторинга.", permissions=['change'])
    def set_is_being_scan_true(self, request, queryset):
        queryset.update(is_being_scan=True)

    @admin.action(description="Поменять статус мониторинга.", permissions=['change'])
    def switch_is_being_true(self, request, queryset):
        for target in models.Target.objects.filter(id__in=queryset.values('id')):
            target.is_being_scan = not target.is_being_scan
            target.save()

    @admin.display(description="Команды мониторинга:")
    def get_monitoring_commands(self, obj):
        try:
            return admin_url_resolver(obj.scrape_command, "record_id", "CMD\t")
        except obj.ObjectDoesNotExist:
            return "N/A"


@admin.register(models.ServerData)
class ServerDataAdmin(admin.ModelAdmin):
    form = forms.ServerDataForm
    fields = ("hostname", "os", "kernel", "server_role", "record_date")
    list_display = ('hostname', 'os', 'kernel', 'server_role', 'get_record_date')
    ordering = ('-record_date',)

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")


@admin.register(models.CPU)
class CPUAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RAM)
class RAMAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiskSpace)
class DiskSpaceAdmin(admin.ModelAdmin):
    list_display = (
        'get_targets', 'file_system', 'fs_size',
        'mounted_on', 'get_record_date'
    )
    ordering = ('-record_date', )

    @admin.action(description="Очистить таблицу DiskSpace.", permissions=["change"])
    def truncate_disk_space(self, request, queryset):
        queryset.delete()

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Сервер:", ordering='target')
    def get_targets(self, obj):
        return admin_url_resolver(obj.target, "id", "Целевой хост\t")


@admin.register(models.NetInterface)
class NetInterfaceAdmin(admin.ModelAdmin):
    list_display = (
        'get_targets',
        'interface', 'ip_address',
        'status', 'get_record_date',
    )
    ordering = ('-record_date',)

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Сервер:", ordering='target')
    def get_targets(self, obj):
        return admin_url_resolver(obj.target, "id", "Целевой хост\t")


@admin.register(models.DashboardSettings)
class DashboardSettingsAdmin(admin.ModelAdmin):
    list_display = ('command_id', 'scraper_url',
                    'scraper_url_health_check', 'scrape_interval')
