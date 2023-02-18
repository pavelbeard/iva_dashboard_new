from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError

from dashboard import models


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
                scrape_command="sudo /usr/sbin/crm status",
                scrape_command_cpu='top -bn 1 -d.2 | grep "Cpu" && top 1 -w 70 -bn 1 | grep -P "^(%)"',
                scrape_command_ram="free -b",
                scrape_command_fs='df && lsblk  -b| grep -E "^sda"',
                scrape_command_apps="/usr/sbin/service --status-all",
                scrape_command_net="/usr/sbin/ifconfig",
                scrape_command_uptime="uptime",
                scrape_command_hostnamectl="uname -n && uname -r && cat /etc/os-release",
                scrape_command_load_average="uptime"
            )
            query.save()
            self.stdout.write(self.style.SUCCESS("Monitoring commands are added to database"))
        except Exception:
            raise CommandError("Scrape commands are added to database.")
            # self.stdout.write(self.style.WARNING())


