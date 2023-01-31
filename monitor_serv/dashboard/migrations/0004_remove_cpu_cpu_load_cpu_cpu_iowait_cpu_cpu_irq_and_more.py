# Generated by Django 4.1.4 on 2023-01-31 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_target_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpu',
            name='cpu_load',
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_iowait',
            field=models.FloatField(default=0, verbose_name='Ожидание ввода/вывода %:'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_irq',
            field=models.FloatField(default=0, verbose_name='Запросы на прерывание %:'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_nice',
            field=models.FloatField(default=0, verbose_name="'Приятная' загрузка процессора %:"),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_softirq',
            field=models.FloatField(default=0, verbose_name='Программные прерывания %:'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_steal',
            field=models.FloatField(default=0, verbose_name='Нехватка времени в ВМ %:'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_sys',
            field=models.FloatField(default=0, verbose_name='Системное время %:'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_user',
            field=models.FloatField(default=0, verbose_name='Пользовательское время %:'),
        ),
        migrations.AddField(
            model_name='target',
            name='is_being_scan',
            field=models.BooleanField(default=True, verbose_name='Сервер сканируется?'),
        ),
    ]
