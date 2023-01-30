from django.db import models
from django.db.models import fields
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.
SERVER_ROLE = (
    ('media', "MEDIA"),
    ('head', "HEAD"),
)


class Target(models.Model):
    class ServerRole(models.TextChoices):
        MEDIA = 'media', _('MEDIA')
        HEAD = 'head', _('HEAD')

    id = fields.AutoField(primary_key=True)
    address = fields.GenericIPAddressField(null=False, verbose_name="IP-адрес целевого сервера:", unique=True)
    port = fields.SmallIntegerField(null=False, verbose_name="Порт сервера:")
    username = fields.CharField(max_length=32, null=False, verbose_name="Логин сервера:")
    password = fields.CharField(max_length=255, null=False, verbose_name="Пароль сервера:")
    server_role = fields.CharField(max_length=6, choices=ServerRole.choices, default=ServerRole.MEDIA,
                                   verbose_name="Роль сервера:")

    class Meta:
        verbose_name = "Целевой хост"
        verbose_name_plural = "Целевые хосты"

    def __str__(self):
        return f"Target(address={self.address}, port={self.port}, username={self.username}, " \
               f"server_role={self.server_role})"


class Server(models.Model):
    hostname = fields.CharField(max_length=64, null=False, default="none", verbose_name="Имя сервера:")
    os = fields.CharField(max_length=32, null=False, default="none", verbose_name="Операционная система:")
    kernel = fields.CharField(max_length=64, null=False, default="none", verbose_name="Ядро ОС:")

    server = models.OneToOneField(Target, on_delete=models.CASCADE, verbose_name="Целевой хост:", primary_key=True)

    class Meta:
        verbose_name = "Данные сервера"
        verbose_name_plural = "Данные сервера"

    def __str__(self):
        return f"Server(hostname={self.hostname}, os={self.os}, kernel={self.kernel})"


class CPU(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    cpu_cores = fields.IntegerField(null=False, default=0, verbose_name="Количество ядер:")
    # cpu_load = fields.FloatField(null=False, default=0, verbose_name="Загрузка процессора %:")
    cpu_idle = fields.FloatField(null=False, default=0, verbose_name="Простой процессора %:")
    cpu_iowait = fields.FloatField(null=False, default=0, verbose_name="Ожидание ввода/вывода %:")
    cpu_irq = fields.FloatField(null=False, default=0, verbose_name="Запросы на прерывание %:")
    cpu_nice = fields.FloatField(null=False, default=0, verbose_name="'Приятная' загрузка процессора %:")
    cpu_softirq = fields.FloatField(null=False, default=0, verbose_name="Программные прерывания %:")
    cpu_steal = fields.FloatField(null=False, default=0, verbose_name="Нехватка времени в ВМ %:")
    cpu_sys = fields.FloatField(null=False, default=0, verbose_name='Системное время %:')
    cpu_user = fields.FloatField(null=False, default=0, verbose_name='Пользовательское время %:')
    record_date = fields.DateTimeField(auto_now=True, null=False, verbose_name="Время сканирования:")

    # TODO: idle, iowait, irq, nice, softirq, steal, system, user

    server_id = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"Server(server_id={self.server_id}, cpu_cores={self.cpu_cores}, " \
               f"cpu_idle={self.cpu_idle}, cpu_iowait={self.cpu_iowait}, " \
               f"cpu_irq={self.cpu_irq}, cpu_nice={self.cpu_nice}, " \
               f"cpu_softirq={self.cpu_softirq}, cpu_steal={self.cpu_steal}, " \
               f"cpu_sys={self.cpu_sys}, cpu_user={self.cpu_user}, " \
               f"record_date={self.record_date})"


# TODO: class LoadAverage:


class RAM(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    total_ram = fields.FloatField(null=False, default=0, verbose_name="Всего RAM:")
    ram_free = fields.FloatField(null=False, default=0, verbose_name="Свободной памяти:")
    ram_used = fields.FloatField(null=False, default=0, verbose_name="Занятой памяти:")
    record_date = fields.DateTimeField(auto_now=True, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"Server(server_id={self.server_id}, total_ram={self.total_ram}, " \
               f"ram_free={self.ram_free}, ram_used={self.ram_used}, record_date={self.record_date})"


class DiskSpace(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    file_system = fields.CharField(null=False, default="none", max_length=128, verbose_name="Файловая система:")
    fs_size = fields.FloatField(null=False, default=0, verbose_name="Размер файловой системы:")
    fs_used = fields.FloatField(null=False, default=0, verbose_name="Занято:")
    fs_used_prc = fields.FloatField(null=False, default=0, verbose_name="Занято в %:")
    fs_avail = fields.FloatField(null=False, default=0, verbose_name="Доступно:")
    mounted_on = fields.CharField(null=False, default="none", max_length=128, verbose_name="Подключено к:")
    record_date = fields.DateTimeField(auto_now=True, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"Server(server_id={self.server_id}, file_system={self.file_system}, " \
               f"fs_size={self.fs_size}, fs_used={self.fs_used}, fs_used_prc={self.fs_used_prc} " \
               f"fs_avail={self.fs_avail}, mounted_on={self.mounted_on}" \
               f"record_date={self.record_date})"


class NetInterface(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)
    interface = fields.CharField(null=False, default="null", max_length=32, verbose_name="Интерфейс:")
    status = fields.CharField(null=False, default="null", max_length=4, verbose_name="Состояние:")
    ip_address = fields.GenericIPAddressField(null=False, default="0.0.0.0", verbose_name="IP-адрес интерфейса:")
    rx_bytes = fields.FloatField(null=False, default=0, verbose_name="Получено байтов:")
    rx_packets = fields.FloatField(null=False, default=0, verbose_name="Получено пакетов:")
    rx_errors_dropped = fields.FloatField(null=False, default=0, verbose_name="Отброшено пакетов:")
    rx_errors_overruns = fields.FloatField(null=False, default=0, verbose_name='Перерасходованных пакетов:')
    rx_errors_frame = fields.FloatField(null=False, default=0, verbose_name='Неправильных кадров:')
    tx_bytes = fields.FloatField(null=False, default=0, verbose_name="Отправлено байтов:")
    tx_packets = fields.FloatField(null=False, default=0, verbose_name="Отправлено пакетов:")
    tx_errors_errors = fields.FloatField(null=False, default=0, verbose_name="Отправлено с ошибками:")
    tx_errors_dropped = fields.FloatField(null=False, default=0, verbose_name="Отброшено при отправке пакетов:")
    tx_errors_overruns = fields.FloatField(null=False, default=0,
                                           verbose_name="Перерасходованных при отправке пакетов:")
    tx_errors_carrier = fields.FloatField(null=False, default=0, verbose_name='Пакетов с потерянными носителями :')
    tx_errors_collisions = fields.FloatField(null=False, default=0, verbose_name="Отправлено пакетов с коллизиями:")
    record_date = fields.DateTimeField(auto_now=True, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"Server(server_id={self.server_id}, interface={self.interface}, " \
               f"status={self.status}, ip_address={self.ip_address}, rx_bytes={self.rx_bytes}, " \
               f"rx_packets={self.rx_packets}, rx_errors_dropped={self.rx_errors_dropped}, " \
               f"rx_errors_overruns={self.rx_errors_overruns}, rx_errors_frame={self.rx_errors_frame}, " \
               f"tx_bytes={self.tx_bytes}, tx_packets={self.tx_packets}, tx_errors_errors={self.tx_errors_errors}, " \
               f"tx_errors_dropped={self.tx_errors_dropped}, tx_errors_overruns={self.tx_errors_overruns}, " \
               f"tx_errors_carrier={self.tx_errors_carrier}, tx_errors_collisions={self.tx_errors_collisions}, " \
               f"record_date={self.record_date})"

    # TODO: Закончить перевод полей для verbose_names

# Не нужно
# class Services(models.Model):
#     uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True)
