# Generated by Django 4.2.10 on 2024-02-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis_relations", "0005_alter_property_obj_class_alter_property_subj_class"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="name_forward",
            field=models.CharField(
                help_text='Inverse relation like: "is sub-class of" vs. "is super-class of".',
                max_length=255,
                verbose_name="Name forward",
            ),
        ),
    ]
