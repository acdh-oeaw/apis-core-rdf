# Generated by Django 4.2.10 on 2024-03-15 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apis_metainfo", "0011_alter_rootobject_deprecated_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rootobject",
            name="deprecated_name",
        ),
    ]
