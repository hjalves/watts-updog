from django.contrib import admin

from metrics.models import Metric, FloatMeasurement, StringMeasurement


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('device', 'type', 'data_type', 'mqtt_topic')


@admin.register(FloatMeasurement)
class FloatMeasurementAdmin(admin.ModelAdmin):
    list_display = ('time', 'metric', 'value')


@admin.register(StringMeasurement)
class StringMeasurementAdmin(admin.ModelAdmin):
    list_display = ('time', 'metric', 'value')

