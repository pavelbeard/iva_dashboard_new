# Generated by Django 4.1.4 on 2023-02-02 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_dashboardsettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='id',
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='command_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]