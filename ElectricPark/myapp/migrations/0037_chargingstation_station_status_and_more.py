# Generated by Django 4.2.3 on 2023-08-31 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0036_delete_banana"),
    ]

    operations = [
        migrations.AddField(
            model_name="chargingstation",
            name="station_status",
            field=models.CharField(
                choices=[("Used", "Used"), ("Available", "Available")],
                default="Available",
                max_length=10,
                verbose_name="station status",
            ),
        ),
        migrations.AddField(
            model_name="chargingstation",
            name="working_hours_finish",
            field=models.TimeField(null=True, verbose_name="working hours finish"),
        ),
        migrations.AddField(
            model_name="chargingstation",
            name="working_hours_start",
            field=models.TimeField(null=True, verbose_name="working hours start"),
        ),
    ]
