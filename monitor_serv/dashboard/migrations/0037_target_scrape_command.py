# Generated by Django 4.1.4 on 2023-02-07 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_remove_target_scrape_command'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='scrape_command',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.scrapecommand', verbose_name='Набор команд мониторинга:'),
        ),
    ]
