from dashboard.models import DashboardSettings as Settings
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Настраивает сервер мониторинга"
    #
    # def add_arguments(self, parser):
    #     parser.add_argument('setupdashboard')

    def handle(self, *args, **options):
        try:
            query = Settings.objects.create(
                command_id=1,
                scraper_url=settings.SCRAPER_URL,
                scraper_url_health_check=settings.SCRAPER_HEALTH_CHECK,
                scrape_interval=int(settings.SCRAPE_INTERVAL)
            )
            query.save()
            self.stdout.write(self.style.SUCCESS("The monitoring server has been successful configured"))
        except IntegrityError:
            raise CommandError(
                "The monitoring server has been configured, if you want to reset configuration"
                "type 'resetdashboardsettings'."
            )

