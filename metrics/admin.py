from django.contrib import admin

from metrics.models import Metric, FloatMeasurement, StringMeasurement


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("__str__", "device", "data_type", "mqtt_topic")
    readonly_fields = ("full_mqtt_topic",)

    def full_mqtt_topic(self, obj):
        return obj.full_mqtt_topic

    full_mqtt_topic.short_description = "MQTT topic (full)"


@admin.register(FloatMeasurement)
class FloatMeasurementAdmin(admin.ModelAdmin):
    list_display = ("time", "value", "metric")
    list_filter = ('metric__type', )
    date_hierarchy = "time"


@admin.register(StringMeasurement)
class StringMeasurementAdmin(admin.ModelAdmin):
    list_display = ("time", "value", "metric")
    list_filter = ('metric__type', )
    date_hierarchy = "time"
