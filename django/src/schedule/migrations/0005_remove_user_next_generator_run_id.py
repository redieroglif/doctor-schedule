# Generated by Django 2.2 on 2021-07-31 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20210730_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='next_generator_run_id',
        ),
    ]