from django.contrib import admin

from devices.models import DeviceType, Device


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "home", "mqtt_topic")
    readonly_fields = ("full_mqtt_topic", )

    def full_mqtt_topic(self, obj):
        return obj.full_mqtt_topic

    full_mqtt_topic.short_description = "MQTT topic (full)"
