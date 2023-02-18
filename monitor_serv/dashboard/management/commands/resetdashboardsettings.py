from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from dashboard.models import DashboardSettings as Settings


class Command(BaseCommand):
    help = "Сбрасывает настройки сервера мониторинга."

    def handle(self, *args, **options):
        try:
            query = Settings.objects.get(command_id=1)
            query.delete()
            self.stdout.write(self.style.SUCCESS("The monitor server settings are reseted."))
        except Settings.DoesNotExist:
            raise CommandError(
                "The monitoring server has been reseted, if you want to add commands type 'setupdashboard'."
            )
