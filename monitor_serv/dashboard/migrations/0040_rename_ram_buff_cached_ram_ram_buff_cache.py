# Generated by Django 4.1.4 on 2023-02-08 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0039_alter_cpu_options_alter_diskspace_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ram',
            old_name='ram_buff_cached',
            new_name='ram_buff_cache',
        ),
    ]