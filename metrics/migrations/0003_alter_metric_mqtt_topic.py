# Generated by Django 4.2 on 2023-04-15 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("metrics", "0002_alter_floatmeasurement_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="metric",
            name="mqtt_topic",
            field=models.CharField(max_length=50, verbose_name="MQTT topic"),
        ),
    ]