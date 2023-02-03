from django.db import models
from django.db.models import fields
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
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
    server_role = fields.CharField(
        max_length=6, choices=ServerRole.choices, default=ServerRole.MEDIA,
        verbose_name="Роль сервера:"
    )
    is_being_scan = fields.BooleanField(default=True, verbose_name="Сервер сканируется?")

    def __str__(self):
        return f"Target(id={self.id}, ip={self.address}, port={self.port})"

    class Meta:
        verbose_name = "Целевой хост"
        verbose_name_plural = "1.Целевые хосты"
        app_label = "dashboard"


class ServerData(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    hostname = fields.CharField(max_length=64, blank=True, verbose_name="Имя сервера:")
    os = fields.CharField(max_length=32, blank=True, verbose_name="Операционная система:")
    kernel = fields.CharField(max_length=64, blank=True, verbose_name="Ядро ОС:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"ServerData(server_id={self.server_id_id}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Данные сервера"
        verbose_name_plural = "2.Данные серверов"
        app_label = "dashboard"


class CPU(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    cpu_cores = fields.IntegerField(null=False, default=0, verbose_name="Количество ядер:")
    cpu_idle = fields.FloatField(null=False, default=0, verbose_name="Простой процессора, id %:")
    cpu_iowait = fields.FloatField(null=False, default=0, verbose_name="Ожидание ввода/вывода, wa %:")
    cpu_irq = fields.FloatField(null=False, default=0, verbose_name="Запросы на прерывание, hi %:")
    cpu_nice = fields.FloatField(null=False, default=0, verbose_name="'Приятная' загрузка процессора, ni %:")
    cpu_softirq = fields.FloatField(null=False, default=0, verbose_name="Программные прерывания, si %:")
    cpu_steal = fields.FloatField(null=False, default=0, verbose_name="Нехватка времени в ВМ, st %:")
    cpu_sys = fields.FloatField(null=False, default=0, verbose_name='Системное время, sy %:')
    cpu_user = fields.FloatField(null=False, default=0, verbose_name='Пользовательское время, us %:')
    cpu_util = fields.FloatField(null=False, default=0, verbose_name="Загрузка процессора %:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"CPU(server_id={self.server_id_id}, cpu_util={self.cpu_util}, " \
               f"cpu_cores={self.cpu_cores}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Данные процессора"
        verbose_name_plural = "3.Данные процессоров"
        app_label = "dashboard"


class RAM(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    total_ram = fields.FloatField(null=False, default=0, verbose_name="Всего RAM:")
    ram_used = fields.FloatField(null=False, default=0, verbose_name="Занятой памяти:")
    ram_free = fields.FloatField(null=False, default=0, verbose_name="Свободной памяти:")
    ram_shared = fields.FloatField(null=False, default=0, verbose_name="Общей памяти:")
    ram_buff_cached = fields.FloatField(null=False, default=0, verbose_name="Буферизованной/кэшированной памяти:")
    ram_avail = fields.FloatField(null=False, default=0, verbose_name="Доступной памяти:")
    ram_util = fields.FloatField(null=False, default=0, verbose_name="Загрузка памяти %:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"RAMData(server_id={self.server_id_id}, total_ram={self.total_ram},  " \
               f"ram_free={self.ram_free}, ram_util={self.ram_util}, record_date={self.record_date}, )"

    class Meta:
        verbose_name = "Данные ОЗУ"
        verbose_name_plural = "4.Данные ОЗУ"
        app_label = "dashboard"


class DiskSpace(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    file_system = fields.CharField(null=False, default="none", max_length=128, verbose_name="Файловая система:")
    fs_size = fields.CharField(null=False, max_length=10, default="none", verbose_name="Размер файловой системы:")
    fs_used = fields.CharField(null=False, max_length=10, default="none", verbose_name="Занято:")
    fs_used_prc = fields.FloatField(null=False, default=0, verbose_name="Занято в %:")
    fs_avail = fields.CharField(null=False, max_length=10, default="none", verbose_name="Доступно:")
    mounted_on = fields.CharField(null=False, default="none", max_length=128, verbose_name="Подключено к:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"FileSystemData(server_id={self.server_id_id}, fs={self.file_system}, " \
               f"fs_size={self.fs_size}, fs_used={self.fs_used}, fs_used%={self.fs_used_prc}," \
               f" record_date={self.record_date}, )"

    class Meta:
        verbose_name = "Данные файлового накопителя"
        verbose_name_plural = "5.Данные файловых накопителей"
        app_label = "dashboard"


class NetInterface(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    interface = fields.CharField(null=False, default="null", max_length=32, verbose_name="Интерфейс:")
    status = fields.CharField(null=False, default="null", max_length=4, verbose_name="Состояние:")
    ip_address = fields.GenericIPAddressField(null=False, default="0.0.0.0", verbose_name="IP-адрес интерфейса:")
    rx_bytes = fields.FloatField(null=False, default=0, verbose_name="Получено байтов:")
    rx_packets = fields.FloatField(null=False, default=0, verbose_name="Получено пакетов:")
    rx_errors_errors = fields.IntegerField(null=False, default=0, verbose_name="Пакетов с ошибками:")
    rx_errors_dropped = fields.IntegerField(null=False, default=0, verbose_name="Отброшено пакетов:")
    rx_errors_overruns = fields.IntegerField(null=False, default=0, verbose_name='Перерасходованных пакетов:')
    rx_errors_frame = fields.IntegerField(null=False, default=0, verbose_name='Неправильных кадров:')
    tx_bytes = fields.FloatField(null=False, default=0, verbose_name="Отправлено байтов:")
    tx_packets = fields.FloatField(null=False, default=0, verbose_name="Отправлено пакетов:")
    tx_errors_errors = fields.IntegerField(null=False, default=0, verbose_name="Отправлено с ошибками:")
    tx_errors_dropped = fields.IntegerField(null=False, default=0, verbose_name="Отброшено при отправке пакетов:")
    tx_errors_overruns = fields.IntegerField(null=False, default=0,
                                             verbose_name="Перерасходованных при отправке пакетов:")
    tx_errors_carrier = fields.IntegerField(null=False, default=0, verbose_name='Пакетов с потерянными носителями :')
    tx_errors_collisions = fields.IntegerField(null=False, default=0, verbose_name="Отправлено пакетов с коллизиями:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    server_id = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"NetInterface(server_id={self.server_id_id}, iface={self.interface}, ip={self.ip_address}, " \
               f"status={self.status}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Данные сетевых интерфейсов"
        verbose_name_plural = "6.Данные сетевых интерфейсов"
        app_label = "dashboard"


class DashboardSettings(models.Model):
    command_id = fields.IntegerField(primary_key=True, editable=False)
    scraper_url = fields.CharField(max_length=255, blank=True, verbose_name="URL агента мониторинга")
    scrape_interval = fields.IntegerField(default=15, verbose_name="Интервал снятия метрик:")

    def __str__(self):
        return f"Settings(scraper_url={self.scraper_url}, scrape_interval={self.scrape_interval})"

    class Meta:
        verbose_name = "Настройки сервера"
        verbose_name_plural = "Настройки сервера"
        app_label = "dashboard"
