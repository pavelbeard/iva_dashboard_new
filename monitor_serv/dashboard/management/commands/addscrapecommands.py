from dashboard import models
from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Записывает в БД команды мониторинга"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--help'
    #     )

    def handle(self, *args, **options):
        try:
            query = models.ScrapeCommand.objects.create(
                record_id=0,
                scrape_command={"crm": 'sudo /usr/sbin/crm status',
                                "cpu": 'top -bn 1 -d.2 | grep "Cpu" && top 1 -w 70 -bn 1 | grep -P "^(%)"',
                                "ram": 'free -b',
                                "fs": 'df && lsblk  -b| grep -E "^sda"',
                                "apps": '/usr/sbin/service --status-all',
                                "net": '/usr/sbin/ifconfig',
                                "server_data": 'uname -n && uname -r && cat /etc/os-release',
                                "uptime": 'uptime',
                                "load_average": 'uptime'}
            )
            query.save()
            self.stdout.write(self.style.SUCCESS("Monitoring commands are added to database"))
        except Exception:
            raise CommandError("Scrape commands are added to database.")
            # self.stdout.write(self.style.WARNING())
