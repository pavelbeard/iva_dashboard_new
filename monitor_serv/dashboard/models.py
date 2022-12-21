from django.db import models
from django.db.models import fields
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.
SERVER_ROLE = (
    ('media', "MEDIA"),
    ('slave', "SLAVE"),
    ('master', "MASTER"),
)


class Target(models.Model):
    class ServerRole(models.TextChoices):
        MEDIA = 'media', _('MEDIA')
        SLAVE = 'slave', _('SLAVE')
        MASTER = 'master', _('MASTER')

    uuid = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    address = fields.GenericIPAddressField(null=False, verbose_name="IP-адрес целевого сервера:")
    port = fields.SmallIntegerField(null=False, verbose_name="Порт сервера:")
    username = fields.CharField(max_length=32, null=False, verbose_name="Логин сервера:")
    password = fields.CharField(max_length=32, null=False, verbose_name="Пароль сервера:")
    server_role = fields.CharField(max_length=6, choices=ServerRole.choices, default=ServerRole.MEDIA,
                                   verbose_name="Роль сервера:")

    def __str__(self):
        return f"Target(address={self.address}, port={self.port}, username={self.username}, " \
               f"server_role={self.server_role})"


class Server(models.Model):
    uuid = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    hostname = fields.CharField(max_length=64, null=False, verbose_name="Имя сервера:")
    address = fields.GenericIPAddressField(null=False, verbose_name="IP-адрес сервера:")
    os = fields.CharField(max_length=32, null=False, verbose_name="Операционная система:")
    kernel = fields.CharField(max_length=64, null=False, verbose_name="Ядро ОС:")

    def __str__(self):
        return f"Server(hostname={self.hostname}, address={self.address}, os={self.os}, kernel={self.kernel})"


class CPU(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    cpu_cores = fields.IntegerField(null=False, verbose_name="Количество ядер:")
    cpu_load = fields.FloatField(null=False, verbose_name="Загрузка процессора %:")
    cpu_idle = fields.FloatField(null=False, verbose_name="Простой процессора %:")
    record_date = fields.DateTimeField(auto_now=True, null=False, verbose_name="Информация взята:")

    server_uuid = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name="Сервер:")


class RAM(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)


class DiskSpace(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)


class NetInterface(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)
