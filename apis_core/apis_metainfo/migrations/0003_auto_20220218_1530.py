# Generated by Django 3.1.14 on 2022-02-18 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis_metainfo", "0002_auto_20220201_1241"),
    ]

    operations = [
        migrations.AlterField(
            model_name="text",
            name="text",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
    ]
