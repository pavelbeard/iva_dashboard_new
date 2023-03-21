from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import fields


# Create your models here.

class Target(models.Model):
    address = fields.GenericIPAddressField(null=False, verbose_name="IP-адрес целевого сервера:")
    port = fields.SmallIntegerField(null=False, verbose_name="Порт сервера:")

    def __str__(self):
        return f"Target host {self.address}"

    class Meta:
        verbose_name = "целевой хост"
        verbose_name_plural = "целевые хосты"
        app_label = "dashboard"
        unique_together = ("address", "port")


class DashboardSettings(models.Model):
    address_for_check_ssl = fields.TextField()
    port = fields.SmallIntegerField()

    def __str__(self):
        return f"dashboard settings {self.id}"

    class Meta:
        verbose_name = 'настройки дашборда'
        verbose_name_plural = 'настройки дашборда'
        app_label = 'dashboard'
