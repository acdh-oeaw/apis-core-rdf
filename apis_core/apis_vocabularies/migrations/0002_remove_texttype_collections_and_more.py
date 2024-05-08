# Generated by Django 4.2.8 on 2023-12-22 07:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("apis_vocabularies", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="texttype",
            name="collections",
        ),
        migrations.RemoveField(
            model_name="texttype",
            name="vocabsbaseclass_ptr",
        ),
        migrations.RemoveField(
            model_name="vocabnames",
            name="name",
        ),
        migrations.RemoveField(
            model_name="vocabsbaseclass",
            name="description",
        ),
        migrations.RemoveField(
            model_name="vocabsbaseclass",
            name="parent_class",
        ),
        migrations.RemoveField(
            model_name="vocabsbaseclass",
            name="status",
        ),
        migrations.RemoveField(
            model_name="vocabsbaseclass",
            name="userAdded",
        ),
        migrations.RemoveField(
            model_name="vocabsbaseclass",
            name="vocab_name",
        ),
        migrations.RemoveField(
            model_name="vocabsuri",
            name="domain",
        ),
        migrations.RemoveField(
            model_name="vocabsuri",
            name="loaded",
        ),
        migrations.RemoveField(
            model_name="vocabsuri",
            name="loaded_time",
        ),
        migrations.RemoveField(
            model_name="vocabsuri",
            name="rdf_link",
        ),
        migrations.RemoveField(
            model_name="vocabsuri",
            name="uri",
        ),
        migrations.RemoveField(
            model_name="vocabsuri",
            name="vocab",
        ),
        migrations.DeleteModel(
            name="LabelType",
        ),
        migrations.DeleteModel(
            name="TextType",
        ),
    ]
