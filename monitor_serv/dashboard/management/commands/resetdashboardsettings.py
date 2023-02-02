from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from dashboard.models import DashboardSettings as Settings


class Command(BaseCommand):
    help = "Сбрасывает настройки сервера мониторинга"
    #
    # def add_arguments(self, parser):
    #     parser.add_argument('resetdashboardsettings')

    def handle(self, *args, **options):
        try:
            query = Settings.objects.get(command_id=1)
            query.delete()
            self.stdout.write(self.style.SUCCESS("Настройки сервера мониторинга успешно сброшены."))
        except Settings.DoesNotExist:
            raise CommandError(
                "Сервер мониторинга уже сброшен, чтобы настроить сервер введите: setupdashboard."
            )
