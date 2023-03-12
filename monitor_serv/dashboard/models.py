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


class PromQL(models.Model):
    query = fields.TextField()

    fk_target = models.ForeignKey(Target, related_name='fk_target', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"query for [{self.fk_target.address}]={self.query}"


class BackendSettings(models.Model):
    refresh_interval = fields.SmallIntegerField(null=False)

    def __str__(self):
        return f"dashboard refresh interval: {self.refresh_interval}"


# class Settings(models.Model):
#     refresh_interval = fields.SmallIntegerField(null=False, verbose_name="Порт сервера:")
#
#     def __str__(self):
#         return f"dashboard refresh interval: {self.refresh_interval}"