# Generated by Django 4.1.4 on 2023-02-18 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0051_alter_cpu_options_alter_dashboardsettings_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='scrape_command',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.scrapecommand', verbose_name='Набор команд мониторинга:'),
        ),
    ]
