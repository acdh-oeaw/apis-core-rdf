# Generated by Django 4.2.10 on 2024-03-07 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis_metainfo", "0010_rename_name_rootobject_deprecated_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rootobject",
            name="deprecated_name",
            field=models.CharField(blank=True, max_length=255, verbose_name="Name"),
        ),
    ]
