# Generated by Django 4.2.3 on 2023-08-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0027_alter_car_battery_pack_kwh_alter_car_car_model_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="brand",
            field=models.CharField(max_length=200, verbose_name="Brand"),
        ),
        migrations.AlterField(
            model_name="car",
            name="car_model",
            field=models.CharField(max_length=200, verbose_name="Model"),
        ),
    ]
