# Generated by Django 4.2 on 2023-04-15 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_home_mqtt_topic_alter_home_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="home",
            name="mqtt_topic",
            field=models.CharField(max_length=50, unique=True, verbose_name="MQTT topic"),
        ),
    ]