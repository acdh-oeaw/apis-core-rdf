# Generated by Django 4.2.8 on 2024-01-09 12:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("apis_entities", "0003_remove_tempentityclass_source"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TempEntityClass",
        ),
    ]
