# Generated by Django 5.1.1 on 2024-10-05 14:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0002_alter_skoscollection_options"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="skoscollection",
            constraint=models.CheckConstraint(
                condition=models.Q(("name__contains", "|"), _negated=True),
                name="check_name_pipe",
                violation_error_message="The name must not contain the pipe symbol: |",
            ),
        ),
    ]
