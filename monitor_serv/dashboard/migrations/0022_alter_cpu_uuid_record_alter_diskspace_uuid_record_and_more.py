# Generated by Django 4.1.4 on 2023-02-02 10:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_alter_cpu_cpu_idle_alter_cpu_cpu_iowait_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='uuid_record',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='diskspace',
            name='uuid_record',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='netinterface',
            name='uuid_record',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ram',
            name='uuid_record',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='serverdata',
            name='uuid_record',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
