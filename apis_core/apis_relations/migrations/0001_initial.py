# Generated by Django 3.1.14 on 2022-02-01 12:41

from django.db import migrations, models
import django.db.models.deletion

import apis_core.apis_relations.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("apis_metainfo", "0002_auto_20220201_1241"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "rootobject_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="apis_metainfo.rootobject",
                    ),
                ),
                (
                    "name_forward",
                    models.CharField(
                        blank=True,
                        help_text='Inverse relation like: "is sub-class of" vs. "is super-class of".',
                        max_length=255,
                        verbose_name="Name reverse",
                    ),
                ),
                (
                    "name_reverse",
                    models.CharField(
                        blank=True,
                        help_text='Inverse relation like: "is sub-class of" vs. "is super-class of".',
                        max_length=255,
                        verbose_name="Name reverse",
                    ),
                ),
                (
                    "obj_class",
                    models.ManyToManyField(
                        limit_choices_to=models.Q(app_label="apis_entities"),
                        related_name="property_set_obj",
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "subj_class",
                    models.ManyToManyField(
                        limit_choices_to=models.Q(app_label="apis_entities"),
                        related_name="property_set_subj",
                        to="contenttypes.ContentType",
                    ),
                ),
            ],
            bases=("apis_metainfo.rootobject",),
        ),
        migrations.CreateModel(
            name="Triple",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "obj",
                    apis_core.apis_relations.models.InheritanceForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="triple_set_from_obj",
                        to="apis_metainfo.rootobject",
                    ),
                ),
                (
                    "prop",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="triple_set_from_prop",
                        to="apis_relations.property",
                    ),
                ),
                (
                    "subj",
                    apis_core.apis_relations.models.InheritanceForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="triple_set_from_subj",
                        to="apis_metainfo.rootobject",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TempTriple",
            fields=[
                (
                    "triple_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="apis_relations.triple",
                    ),
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
            ],
            bases=("apis_relations.triple",),
        ),
    ]