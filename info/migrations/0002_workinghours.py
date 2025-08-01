# Generated by Django 5.2.3 on 2025-07-10 16:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("info", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkingHours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("sat", "Saturday"),
                            ("sun", "Sunday"),
                            ("mon", "Monday"),
                            ("tue", "Tuesday"),
                            ("wed", "Wednesday"),
                            ("thu", "Thursday"),
                            ("fri", "Friday"),
                        ],
                        max_length=3,
                    ),
                ),
                ("open_time", models.TimeField()),
                ("close_time", models.TimeField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
