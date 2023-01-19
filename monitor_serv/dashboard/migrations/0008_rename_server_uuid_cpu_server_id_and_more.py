# Generated by Django 4.1.4 on 2023-01-19 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_diskspace_file_system_diskspace_fs_avail_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cpu',
            old_name='server_uuid',
            new_name='server_id',
        ),
        migrations.RenameField(
            model_name='diskspace',
            old_name='server_uuid',
            new_name='server_id',
        ),
        migrations.RenameField(
            model_name='netinterface',
            old_name='server_uuid',
            new_name='server_id',
        ),
        migrations.RenameField(
            model_name='ram',
            old_name='server_uuid',
            new_name='server_id',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='target_uuid',
            new_name='server_id',
        ),
        migrations.RemoveField(
            model_name='target',
            name='uuid',
        ),
        migrations.AddField(
            model_name='target',
            name='id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='server',
            name='uuid',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
