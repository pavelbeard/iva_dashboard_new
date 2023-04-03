from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import fields


# Create your models here.

class Target(models.Model):
    address = fields.GenericIPAddressField(null=False, verbose_name="IP-адрес целевого сервера:")
    port = fields.SmallIntegerField(null=False, default=11650, verbose_name="Порт prometheus:")
    port_ssh = fields.SmallIntegerField(null=False, default=22, verbose_name="Порт ssh:")
    username = fields.CharField(max_length=32, null=False, default="admin")
    password = fields.CharField(max_length=256, null=True, verbose_name="Пароль сервера:")
    is_being_scan = fields.BooleanField(default=True, verbose_name="Сервер сканируется?")

    def __str__(self):
        return f"Target host {self.address}"

    class Meta:
        verbose_name = "целевой хост"
        verbose_name_plural = "целевые хосты"
        app_label = "dashboard"
        unique_together = ("address", "port", "port_ssh")


class DashboardSettings(models.Model):
    address_for_check_ssl = fields.TextField()
    port = fields.SmallIntegerField()

    def __str__(self):
        return f"dashboard settings {self.id}"

    class Meta:
        verbose_name = 'настройки дашборда'
        verbose_name_plural = 'настройки дашборда'
        app_label = 'dashboard'


class BackendVersion(models.Model):
    version = fields.CharField(null=True, max_length=16)

    def __str__(self):
        return f"Версия приложения: {self.version}"

    class Meta:
        verbose_name = 'версия приложения'
        verbose_name_plural = 'версия приложения'
        app_label = 'dashboard'

