# Generated by Django 4.1.4 on 2023-02-07 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_remove_scrapecommands_uuid_record_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScrapeCommands',
            new_name='ScrapeCommand',
        ),
    ]