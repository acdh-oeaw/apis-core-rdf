# Generated by Django 4.2.11 on 2024-03-27 14:17

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models

import apis_core.apis_relations.models
import apis_core.generic.abc


class Migration(migrations.Migration):
    dependencies = [
        ("apis_metainfo", "0011_alter_rootobject_deprecated_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("apis_relations", "0005_alter_property_obj_class_alter_property_subj_class"),
    ]

    operations = [
        migrations.CreateModel(
            name="VersionTempTriple",
            fields=[
                (
                    "triple_ptr",
                    models.ForeignKey(
                        auto_created=True,
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        parent_link=True,
                        related_name="+",
                        to="apis_relations.triple",
                    ),
                ),
                (
                    "id",
                    models.IntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "version_tag",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "review",
                    models.BooleanField(
                        default=False,
                        help_text="Should be set to True, if the data record holds up quality standards.",
                    ),
                ),
                ("start_date", models.DateField(blank=True, null=True)),
                ("start_start_date", models.DateField(blank=True, null=True)),
                ("start_end_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("end_start_date", models.DateField(blank=True, null=True)),
                ("end_end_date", models.DateField(blank=True, null=True)),
                (
                    "start_date_written",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Start"
                    ),
                ),
                (
                    "end_date_written",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="End"
                    ),
                ),
                ("status", models.CharField(max_length=100)),
                ("references", models.TextField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
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
                (
                    "obj",
                    apis_core.apis_relations.models.InheritanceForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="apis_metainfo.rootobject",
                        verbose_name="Object",
                    ),
                ),
                (
                    "prop",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="apis_relations.property",
                        verbose_name="Property",
                    ),
                ),
                (
                    "subj",
                    apis_core.apis_relations.models.InheritanceForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="apis_metainfo.rootobject",
                        verbose_name="Subject",
                    ),
                ),
            ],
            options={
                "verbose_name": "Version",
                "verbose_name_plural": "Versions",
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
