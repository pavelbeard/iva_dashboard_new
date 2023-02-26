# Generated by Django 4.1.4 on 2023-02-01 10:58

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_cpu_options_alter_diskspace_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='hostname',
        ),
        migrations.RemoveField(
            model_name='target',
            name='kernel',
        ),
        migrations.RemoveField(
            model_name='target',
            name='os',
        ),
        migrations.CreateModel(
            name='ServerData',
            fields=[
                ('uuid_record', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('hostname', models.CharField(blank=True, editable=False, max_length=64, verbose_name='Имя сервера:')),
                ('os', models.CharField(blank=True, editable=False, max_length=32, verbose_name='Операционная система:')),
                ('kernel', models.CharField(blank=True, editable=False, max_length=64, verbose_name='Ядро ОС:')),
                ('record_date', models.DateTimeField(auto_now=True, verbose_name='Время сканирования:')),
                ('server_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.target', verbose_name='Сервер:')),
            ],
            options={
                'verbose_name': 'Данные сервера',
                'verbose_name_plural': 'Данные серверов',
            },
        ),
    ]
