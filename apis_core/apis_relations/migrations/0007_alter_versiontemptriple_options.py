# Generated by Django 5.1 on 2024-09-18 06:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("apis_relations", "0006_versiontemptriple"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="versiontemptriple",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical temp triple",
                "verbose_name_plural": "historical temp triples",
            },
        ),
    ]
