# Generated by Django 4.1.4 on 2023-02-10 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0044_alter_serverdata_server_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='netinterface',
            options={'verbose_name': 'Данные сетевых интерфейсов', 'verbose_name_plural': 'Данные сетевых интерфейсов'},
        ),
    ]