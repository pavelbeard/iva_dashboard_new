# Generated by Django 4.1.4 on 2023-03-03 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0055_remove_scrapecommand_scrape_command_apps_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='netinterface',
            name='status',
            field=models.CharField(default='none', max_length=64, verbose_name='Состояние:'),
        ),
    ]
