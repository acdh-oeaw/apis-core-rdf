# Generated by Django 3.1.14 on 2022-02-01 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("apis_metainfo", "0001_initial"),
        ("apis_vocabularies", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="text",
            name="kind",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="apis_vocabularies.texttype",
            ),
        ),
        migrations.AddField(
            model_name="text",
            name="source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="apis_metainfo.source",
            ),
        ),
        migrations.AddField(
            model_name="rootobject",
            name="self_content_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="collection",
            name="collection_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="apis_vocabularies.collectiontype",
            ),
        ),
        migrations.AddField(
            model_name="collection",
            name="groups_allowed",
            field=models.ManyToManyField(to="auth.Group"),
        ),
        migrations.AddField(
            model_name="collection",
            name="parent_class",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="apis_metainfo.collection",
            ),
        ),
    ]
