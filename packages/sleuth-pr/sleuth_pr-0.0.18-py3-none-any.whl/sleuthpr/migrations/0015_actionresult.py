# Generated by Django 3.1.1 on 2020-10-10 06:48
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("sleuthpr", "0014_auto_20201009_2319"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActionResult",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("success", "Success"),
                            ("failure", "Failure"),
                            ("pending", "Pending"),
                            ("error", "Error"),
                        ],
                        db_index=True,
                        max_length=50,
                    ),
                ),
                ("message", models.TextField(blank=True, max_length=16384, verbose_name="message")),
                (
                    "on",
                    models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name="created on"),
                ),
                (
                    "action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="sleuthpr.action",
                        verbose_name="action",
                    ),
                ),
                (
                    "commit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions_results",
                        to="sleuthpr.repositorycommit",
                        verbose_name="commit",
                    ),
                ),
            ],
        ),
    ]
