# Generated by Django 4.1.4 on 2023-02-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_remove_scrapecommands_record_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapecommands',
            name='uuid_record',
        ),
        migrations.AddField(
            model_name='scrapecommands',
            name='record_id',
            field=models.IntegerField(default=0, editable=False, primary_key=True, serialize=False),
        ),
    ]
