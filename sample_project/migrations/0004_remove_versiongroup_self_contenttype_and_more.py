# Generated by Django 5.1.4 on 2025-02-19 17:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sample_project", "0003_alter_versiongroup_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="versiongroup",
            name="self_contenttype",
        ),
        migrations.RemoveField(
            model_name="versionperson",
            name="self_contenttype",
        ),
        migrations.RemoveField(
            model_name="versionplace",
            name="self_contenttype",
        ),
    ]
