from cryptography.fernet import Fernet
from django.core.management.base import BaseCommand, CommandError
from dashboard.models import DashboardSettings as Settings


class Command(BaseCommand):
    help = "Генерирует секретный ключ шифрования паролей целевых хостов."
    #
    # def add_arguments(self, parser):
    #     parser.add_argument('resetdashboardsettings')

    def handle(self, *args, **options):
        key = str(Fernet.generate_key())
        self.stdout.write(self.style.SUCCESS(key))
