# Generated by Django 2.2 on 2021-07-30 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20210730_2128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
