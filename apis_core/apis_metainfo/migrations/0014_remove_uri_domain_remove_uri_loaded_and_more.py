# Generated by Django 5.1 on 2024-09-25 07:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("apis_metainfo", "0013_delete_collection"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="uri",
            name="domain",
        ),
        migrations.RemoveField(
            model_name="uri",
            name="loaded",
        ),
        migrations.RemoveField(
            model_name="uri",
            name="loaded_time",
        ),
        migrations.RemoveField(
            model_name="uri",
            name="rdf_link",
        ),
    ]