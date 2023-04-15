from django.contrib import admin

from devices.models import DeviceType, Device


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "home", "mqtt_topic")


