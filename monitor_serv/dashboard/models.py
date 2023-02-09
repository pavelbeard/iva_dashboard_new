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


class ScrapeCommand(models.Model):
    record_id = fields.IntegerField(primary_key=True, default=0, editable=False)
    scrape_command = fields.CharField(max_length=512, blank=True, verbose_name="Команда мониторинга:")
    scrape_command_cpu = fields.CharField(max_length=128, blank=True, verbose_name="Команда мониторинга CPU:")
    scrape_command_ram = fields.CharField(max_length=128, blank=True, verbose_name="Команда мониторинга RAM:")
    scrape_command_fs = fields.CharField(
        max_length=128, blank=True, verbose_name="Команда мониторинга файловой системы:")
    scrape_command_apps = fields.CharField(
        max_length=128, blank=True, verbose_name="Команда мониторинга приложений:")
    scrape_command_net = fields.CharField(
        max_length=128, blank=True, verbose_name="Команда мониторинга сетевых интерфейсов:")
    scrape_command_uptime = fields.CharField(
        max_length=128, blank=True, verbose_name="Команда мониторинга времени работы:")
    scrape_command_hostnamectl = fields.CharField(
        max_length=128, blank=True, verbose_name="Мониторинг версии ОС, ядра и имени хоста:")

    def __str__(self):
        return f"{self.__class__.__name__}(record_id={self.record_id})"

    class Meta:
        verbose_name = "Набор команд мониторинга"
        verbose_name_plural = "Набор команд мониторинга"


class Target(models.Model):
    class ServerRole(models.TextChoices):
        MEDIA = 'media', _('MEDIA')
        HEAD = 'head', _('HEAD')

    id = fields.AutoField(primary_key=True)
    address = fields.GenericIPAddressField(null=False, verbose_name="IP-адрес целевого сервера:")
    port = fields.SmallIntegerField(null=False, verbose_name="Порт сервера:")
    username = fields.CharField(max_length=32, null=False, verbose_name="Логин сервера:")
    password = fields.CharField(max_length=255, null=False, verbose_name="Пароль сервера:")
    server_role = fields.CharField(
        max_length=6, choices=ServerRole.choices, default=ServerRole.MEDIA,
        verbose_name="Роль сервера:"
    )
    is_being_scan = fields.BooleanField(default=True, verbose_name="Сервер сканируется?")

    scrape_command = models.ForeignKey(
        ScrapeCommand, on_delete=models.DO_NOTHING, verbose_name="Набор команд мониторинга:", null=True)

    def __str__(self):
        # scrape_command_rec_id = "Nothing" if self.scrape_command is None else self.scrape_command.record_id

        return f"Target(id={self.id}, ip={self.address}, port={self.port}, )" \
            # f"{ScrapeCommand.__name__}={scrape_command_rec_id})"

    class Meta:
        verbose_name = "Целевой хост"
        verbose_name_plural = "Целевые хосты"
        app_label = "dashboard"
        unique_together = ("address", "port")


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

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"CPU(target={self.target}, cpu_util={self.cpu_util}, " \
               f"cpu_cores={self.cpu_cores}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Данные процессора"
        verbose_name_plural = "Данные процессоров"
        app_label = "dashboard"


class RAM(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    total_ram = fields.FloatField(null=False, default=0, verbose_name="Всего RAM:")
    ram_used = fields.FloatField(null=False, default=0, verbose_name="Занятой памяти:")
    ram_free = fields.FloatField(null=False, default=0, verbose_name="Свободной памяти:")
    ram_shared = fields.FloatField(null=False, default=0, verbose_name="Общей памяти:")
    ram_buff_cache = fields.FloatField(null=False, default=0, verbose_name="Буферизованной/кэшированной памяти:")
    ram_avail = fields.FloatField(null=False, default=0, verbose_name="Доступной памяти:")
    ram_util = fields.FloatField(null=False, default=0, verbose_name="Загрузка памяти %:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"RAMData(target={self.target}, total_ram={self.total_ram},  " \
               f"ram_free={self.ram_free}, ram_util={self.ram_util}, record_date={self.record_date}, )"

    class Meta:
        verbose_name = "Данные ОЗУ"
        verbose_name_plural = "Данные ОЗУ"
        app_label = "dashboard"


class DiskSpace(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    file_system = fields.CharField(null=False, default="none", max_length=128, verbose_name="Файловая система:")
    fs_size = fields.FloatField(null=False, max_length=10, default="none", verbose_name="Размер файловой системы:")
    fs_used = fields.FloatField(null=False, max_length=10, default="none", verbose_name="Занято:")
    fs_used_prc = fields.FloatField(null=False, default=0, verbose_name="Занято в %:")
    fs_avail = fields.FloatField(null=False, max_length=10, default="none", verbose_name="Доступно:")
    mounted_on = fields.CharField(null=False, default="none", max_length=128, verbose_name="Подключено к:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"FileSystemData(target={self.target}, fs={self.file_system}, " \
               f"fs_size={self.fs_size}, fs_used={self.fs_used}, fs_used%={self.fs_used_prc}," \
               f" record_date={self.record_date}, )"

    class Meta:
        verbose_name = "Данные файлового накопителя"
        verbose_name_plural = "Данные файловых накопителей"
        app_label = "dashboard"


class DiskSpaceStatistics(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    total_disk_size = fields.FloatField(null=False, default=0, verbose_name="Всего места на диске:")
    most_valuable_part_fs = fields.CharField(
        max_length=128, default="none", verbose_name="Самая 'лучший' раздел файловая система:")
    most_valuable_part_size = fields.IntegerField(
        null=False, default=0, verbose_name="Размер 'лучшего' раздела файловой системы")
    most_valuable_part_used = fields.IntegerField(
        null=False, default=0, verbose_name="Используемый размер 'лучшего' раздела файловой системы")
    most_valuable_part_available = fields.IntegerField(
        null=False, default=0, verbose_name="Доступный размер 'лучшего' раздела файловой системы")
    most_valuable_part_use_percent = fields.CharField(
        max_length=4, default="none", verbose_name="Доступный размер 'лучшего' раздела файловой системы %"
    )
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"FileSystemStatistics(target={self.target}, total_disk_size={self.total_disk_size}, " \
               f"mvp_fs={self.most_valuable_part_fs}, mvp_fs_size={self.most_valuable_part_size}, " \
               f"record_date={self.record_date}, )"

    class Meta:
        verbose_name = "Статистика файловой системы"
        verbose_name_plural = "Статистика файловой системы"
        app_label = "dashboard"


class NetInterface(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    interface = fields.CharField(null=False, default="none", max_length=32, verbose_name="Интерфейс:")
    status = fields.CharField(null=False, default="none", max_length=4, verbose_name="Состояние:")
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

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"NetInterface(target={self.target}, iface={self.interface}, ip={self.ip_address}, " \
               f"status={self.status}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Данные сетевых интерфейсов"
        verbose_name_plural = "6.Данные сетевых интерфейсов"
        app_label = "dashboard"


class ServerData(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    hostname = fields.CharField(max_length=64, blank=True, verbose_name="Имя сервера:")
    os = fields.CharField(max_length=32, blank=True, verbose_name="Операционная система:")
    kernel = fields.CharField(max_length=64, blank=True, verbose_name="Ядро ОС:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"ServerData(target={self.target}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Данные сервера"
        verbose_name_plural = "Данные серверов"
        app_label = "dashboard"


class Process(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    process_name = fields.CharField(max_length=64, default="none", verbose_name="Имя процесса:")
    process_status = fields.CharField(max_length=16, default="none", verbose_name="Статус:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def _x_str__(self):
        return f"{self.__class__.__name__}(target={self.target}, process_name={self.process_name}, " \
               f"process_status={self.process_status}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Статистика файловой системы"
        verbose_name_plural = "Статистика файловой системы"
        app_label = "dashboard"


class Uptime(models.Model):
    uuid_record = fields.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    uptime = fields.CharField(max_length=32, default="none", verbose_name="Время работы сервера:")
    record_date = fields.DateTimeField(default=timezone.now, null=False, verbose_name="Время сканирования:")

    target = models.ForeignKey(Target, on_delete=models.CASCADE, verbose_name="Сервер:")

    def __str__(self):
        return f"{self.__class__.__name__}(uuid_record={self.uuid_record}, record_date={self.record_date})"

    class Meta:
        verbose_name = "Время работы сервера"
        verbose_name_plural = "Время работы серверов"
        app_label = "dashboard"
