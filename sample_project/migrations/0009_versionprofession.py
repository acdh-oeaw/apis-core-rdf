# Generated by Django 5.1.8 on 2025-06-04 05:22

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models

import apis_core.generic.abc


class Migration(migrations.Migration):
    dependencies = [
        ("sample_project", "0008_remove_versiongroup_version_tag_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VersionProfession",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(blank=True, default="", max_length=1024)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical profession",
                "verbose_name_plural": "historical professions",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(
                simple_history.models.HistoricalChanges,
                models.Model,
                apis_core.generic.abc.GenericModel,
            ),
        ),
    ]
