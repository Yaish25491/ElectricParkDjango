# Generated by Django 4.2.3 on 2023-08-05 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_item"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cars",
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
                ("maker", models.CharField(max_length=200)),
                ("car_model", models.CharField(max_length=200)),
                ("car_submodel", models.CharField(max_length=200)),
            ],
        ),
    ]
