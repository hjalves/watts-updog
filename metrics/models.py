from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.formats import localize

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
        (METRIC_TARIFF, "Active tariff"),
        (METRIC_VOLTAGE, "Voltage (V)"),
        (METRIC_FREQUENCY, "Frequency (Hz)"),
        (METRIC_CURRENT, "Frequency (A)"),
    )

    DATA_TYPE_FLOAT = "float"
    DATA_TYPE_STRING = "string"
    DATA_TYPE_CHOICES = (
        (DATA_TYPE_FLOAT, "Float"),
        (DATA_TYPE_STRING, "String"),
    )

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    type = models.CharField(choices=METRIC_TYPE_CHOICES, max_length=10)
    data_type = models.CharField(
        choices=DATA_TYPE_CHOICES, default=DATA_TYPE_FLOAT, max_length=6
    )
    mqtt_topic = models.CharField("MQTT topic", max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "metric"
        verbose_name_plural = "metric"

    def __str__(self):
        return self.get_type_display()

    @property
    def full_mqtt_topic(self):
        return f"{self.device.full_mqtt_topic}/{self.mqtt_topic}"

    def create_measurement(self, value, time=None):
        if time is None:
            time = timezone.now()
        match self.data_type:
            case self.DATA_TYPE_FLOAT:
                value = float(value)
                FloatMeasurement.objects.create(time=time, metric=self, value=value)
            case self.DATA_TYPE_STRING:
                value = str(value)
                StringMeasurement.objects.create(time=time, metric=self, value=value)


class FloatMeasurement(TimescaleModel):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        verbose_name = "measurement (float)"
        verbose_name_plural = "measurements (float)"

    def __str__(self):
        return f"{localize(self.time)} -- {self.value}"


class StringMeasurement(TimescaleModel):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "measurement (string)"
        verbose_name_plural = "measurements (string)"

    def __str__(self):
        return f"{localize(self.time)} -- {self.value}"
