# This migration was generated manually rather than using `python manage.py makemigrations`.
# Reason: [Provide a detailed explanation here, e.g., "Initial schema setup required custom field options not supported by Django's migration autogeneration."]
# Please ensure that any future changes to models are reflected in migrations using the standard Django workflow.
# Manual migrations can lead to inconsistencies; see Django documentation for best practices.
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("location", models.CharField(max_length=255)),
                ("notes", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
