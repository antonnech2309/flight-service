# Generated by Django 5.0.2 on 2024-02-21 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-created_at"]},
        ),
    ]
