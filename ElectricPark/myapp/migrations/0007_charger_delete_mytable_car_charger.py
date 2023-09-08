# Generated by Django 4.2.3 on 2023-08-05 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0006_alter_car_car_model_alter_car_car_submodel_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Charger",
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
                ("type", models.CharField(max_length=200, verbose_name="Maker")),
                ("maker", models.CharField(max_length=200, verbose_name="Model")),
                ("model", models.CharField(max_length=200, verbose_name="Sub Model")),
                ("speed", models.CharField(max_length=200, verbose_name="Sub Model")),
            ],
        ),
        migrations.DeleteModel(
            name="MyTable",
        ),
        migrations.AddField(
            model_name="car",
            name="charger",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.charger",
            ),
        ),
    ]
