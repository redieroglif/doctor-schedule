# Generated by Django 2.2 on 2021-07-29 18:34

from django.db import migrations

def forwards_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).bulk_create([
        Group(name="Doctors"),
        Group(name="Managers"),
        Group(name="Clients"),
    ])

def reverse_func(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).filter(name="Doctors").delete()
    Group.objects.using(db_alias).filter(name="Managers").delete()
    Group.objects.using(db_alias).filter(name="Clients").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]