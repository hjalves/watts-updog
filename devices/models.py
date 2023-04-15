from django.conf import settings
from django.db import models


class DeviceType(models.Model):
    DEVICE_SMART_METER = "smartmeter"
    DEVICE_KIND_CHOICES = ((DEVICE_SMART_METER, "Smart meter"),)
    kind = models.CharField(choices=DEVICE_KIND_CHOICES, max_length=10)

    class Meta:
        verbose_name = "device type"
        verbose_name_plural = "device types"


class Device(models.Model):
    DEVICE_EMI = "emi"
    DEVICE_TYPE_CHOICES = ((DEVICE_EMI, "E-redes EMI"),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
    name = models.CharField(blank=True)

    class Meta:
        verbose_name = "device"
        verbose_name_plural = "devices"
