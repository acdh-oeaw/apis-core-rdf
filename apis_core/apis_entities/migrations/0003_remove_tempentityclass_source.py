# Generated by Django 4.1.10 on 2023-09-21 07:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("apis_entities", "0002_remove_tempentityclass_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tempentityclass",
            name="source",
        ),
    ]
