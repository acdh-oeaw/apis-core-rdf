# Generated by Django 3.1.14 on 2023-01-23 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apis_relations", "0002_property_property_class_uri"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="property",
            options={"verbose_name_plural": "Properties"},
        ),
    ]
