from core_logic.admin import admin_url_resolver
from django.contrib import admin

from . import forms, models


# Register your models here.
@admin.register(models.ScrapeCommand)
class ScrapeCommandAdmin(admin.ModelAdmin):
    form = forms.ScrapeCommandForm


class ServerDataStackInline(admin.StackedInline):
    model = models.ServerData
    list_display = ('hostname', 'os', 'kernel', 'server_role', 'get_record_date')
    ordering = ('-record_date',)
    readonly_fields = ("hostname", "os", "kernel", "server_role", "record_date", 'target')

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")


@admin.register(models.Target)
class TargetAdmin(admin.ModelAdmin):
    form = forms.TargetForm
    list_display = tuple('id address port is_being_scan get_monitoring_commands get_server_data'.split())
    actions = tuple('set_is_being_scan_false set_is_being_scan_true switch_is_being_true'.split())
    inlines = (ServerDataStackInline,)

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

    @admin.display(description="Данные сервера")
    def get_server_data(self, obj: models.Target):
        try:
            return admin_url_resolver(
                obj=obj.serverdata, column="target_id", name="О сервере", hide_column=True)
        except obj.DoesNotExist:
            return "N/A"

    @admin.display(description="Команды мониторинга:")
    def get_monitoring_commands(self, obj):
        try:
            return admin_url_resolver(obj.scrape_command, "record_id", "CMD\t")
        except obj.DoesNotExist:
            return "N/A"


@admin.register(models.ServerData)
class ServerDataAdmin(admin.ModelAdmin):
    form = forms.ServerDataForm
    fields = ("hostname", "os", "kernel", "server_role", "record_date")
    list_display = ('hostname', 'os', 'kernel',
                    'server_role', 'get_record_date', 'get_targets')
    ordering = ('-record_date',)
    readonly_fields = ("hostname", "os", "kernel",
                       "server_role", "record_date", 'target')

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Сервер:", ordering='target')
    def get_targets(self, obj):
        return admin_url_resolver(obj.target, "id", "Целевой хост\t")


@admin.register(models.CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('uuid_record', 'cpu_cores', 'cpu_util',
                    'cpu_idle', 'get_record_date', 'get_targets')
    ordering = ('-record_date',)
    readonly_fields = ("cpu_cores", "cpu_idle", "cpu_iowait",
                       "cpu_irq", "cpu_nice", "cpu_softirq",
                       "cpu_steal", "cpu_sys", "cpu_user",
                       "cpu_util", "record_date", "target")

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Сервер:", ordering='target')
    def get_targets(self, obj):
        return admin_url_resolver(obj.target, "id", f"{obj.target.address}", hide_column=True)


@admin.register(models.RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('uuid_record', 'total_ram', 'ram_used',
                    'ram_free', 'ram_util', 'get_record_date',
                    'get_targets')
    ordering = ('-record_date',)
    readonly_fields = ("total_ram", "ram_used", "ram_free",
                       "ram_shared", "ram_buff_cache", "ram_avail",
                       "ram_util", "record_date", "target")

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Сервер:", ordering='target')
    def get_targets(self, obj):
        return admin_url_resolver(obj.target, "id", f"{obj.target.address}", hide_column=True)


@admin.register(models.DiskSpace)
class DiskSpaceAdmin(admin.ModelAdmin):
    list_display = ('uuid_record', 'file_system', 'fs_size', 'mounted_on', 'get_record_date', 'get_targets')
    ordering = ('-record_date',)
    readonly_fields = ("record_date", "cluster_id", "file_system",
                       "fs_size", "fs_used", "fs_used_prc",
                       "fs_avail", "mounted_on", "record_date",
                       "target", )

    @admin.action(description="Очистить таблицу DiskSpace.", permissions=["change"])
    def truncate_disk_space(self, request, queryset):
        queryset.delete()

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Сервер:", ordering='target')
    def get_targets(self, obj):
        return admin_url_resolver(obj.target, "id", f"{obj.target.address}", hide_column=True)


@admin.register(models.NetInterface)
class NetInterfaceAdmin(admin.ModelAdmin):
    list_display = ('uuid_record', 'interface', 'ip_address', 'status', 'get_record_date', 'get_targets')
    ordering = ('-record_date',)
    readonly_fields = (
        "interface", "status", "ip_address",
        "rx_bytes", "rx_packets", "rx_errors_errors",
        "rx_errors_dropped", "rx_errors_overruns", "rx_errors_frame",
        "tx_bytes", "tx_packets", "tx_errors_errors",
        "tx_errors_dropped", "tx_errors_overruns", "tx_errors_carrier",
        "tx_errors_collisions", "interface_id", "record_date",
        "target",
    )

    @admin.display(description="Время опроса:", ordering='record_date')
    def get_record_date(self, obj):
        return obj.record_date.__format__("%Y-%m-%d %H:%M:%S")

    @admin.display(description="Сервер:", ordering='target')
    def get_targets(self, obj):
        return admin_url_resolver(obj.target, "id", f"{obj.target.address}", hide_column=True)


@admin.register(models.DashboardSettings)
class DashboardSettingsAdmin(admin.ModelAdmin):
    list_display = ('command_id', 'scraper_url',
                    'scraper_url_health_check', 'scrape_interval')
