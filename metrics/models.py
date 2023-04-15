from django.conf import settings
from django.db import models

from timescale.db.models.models import TimescaleModel

from devices.models import Device


class Metric(models.Model):
    METRIC_POWER = "power"
    METRIC_ENERGY_TOTAL = "energy_t"
    METRIC_ENERGY_CHEIAS = "energy_c"
    METRIC_ENERGY_PONTA = "energy_p"
    METRIC_ENERGY_VAZIO = "energy_v"
    METRIC_TARIFF = "tariff"
    METRIC_VOLTAGE = "voltage"
    METRIC_FREQUENCY = "frequency"
    METRIC_CURRENT = "current"
    METRIC_TYPE_CHOICES = (
        (METRIC_POWER, "Power (W)"),
        (METRIC_ENERGY_TOTAL, "Energy total (kWh)"),
        (METRIC_ENERGY_CHEIAS, "Energy cheias (kWh)"),
        (METRIC_ENERGY_PONTA, "Energy ponta (kWh)"),
        (METRIC_ENERGY_VAZIO, "Energy vazio (kWh)"),
        (METRIC_TARIFF, "Tarifa"),
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    type = models.CharField(choices=METRIC_TYPE_CHOICES, max_length=10)

    class Meta:
        verbose_name = "metric"
        verbose_name_plural = "metric"


class FloatMeasurement(TimescaleModel):
    register = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.FloatField()
