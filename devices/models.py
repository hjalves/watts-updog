from django.conf import settings
from django.db import models

from users.models import Home


class DeviceType(models.Model):
    DEVICE_SMART_METER = "smartmeter"
    DEVICE_TYPE_CHOICES = ((DEVICE_SMART_METER, "Smart meter"),)
    kind = models.CharField(choices=DEVICE_TYPE_CHOICES, max_length=10)

    class Meta:
        verbose_name = "device type"
        verbose_name_plural = "device types"

    def __str__(self):
        return self.get_kind_display()


class Device(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    mqtt_topic = models.CharField("MQTT topic", max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "device"
        verbose_name_plural = "devices"

    def __str__(self):
        return self.name

    @property
    def full_mqtt_topic(self):
        return f"{self.home.full_mqtt_topic}/{self.mqtt_topic}"

    def create_metrics(self):
        from metrics.decls import emi_metrics

        for metric_decl in emi_metrics:
            self.metric_set.create(
                type=metric_decl.type,
                data_type=metric_decl.data_type,
                mqtt_topic=metric_decl.mqtt_topic,
            )
