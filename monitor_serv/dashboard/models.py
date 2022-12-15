from django.db import models
from django.db.models import fields
import uuid


# Create your models here.

class Target(models.Model):
    uuid = fields.UUIDField(default=uuid.uuid4().hex, primary_key=True, verbose_name="UUID записи")
    address = fields.GenericIPAddressField(null=False, verbose_name="IP-адрес целевого сервера")
    port = fields.SmallIntegerField(null=False, verbose_name="Порт сервера")
    username = fields.CharField(max_length=32, null=False, verbose_name="Логин сервера")
    password = fields.CharField(max_length=32, null=False, verbose_name="Пароль сервера")


class Server(models.Model):
    uuid = fields.UUIDField(default=uuid.uuid4().hex, primary_key=True)
    hostname = fields.CharField(max_length=64, null=False)
    os = fields.CharField(max_length=32, null=False)
    kernel = fields.CharField(max_length=64, null=False)
