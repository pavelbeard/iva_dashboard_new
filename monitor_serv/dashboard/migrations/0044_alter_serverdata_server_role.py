# Generated by Django 4.1.4 on 2023-02-10 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0043_remove_target_server_role_serverdata_server_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverdata',
            name='server_role',
            field=models.CharField(blank=True, choices=[('media', 'MEDIA'), ('head', 'HEAD')], max_length=6, verbose_name='Роль сервера:'),
        ),
    ]
