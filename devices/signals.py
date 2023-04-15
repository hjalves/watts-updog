from django.db.models.signals import post_save
from django.dispatch import receiver

from devices.models import Device
from metrics.models import Metric
from metrics.decls import emi_metrics


@receiver(post_save, sender=Device)
def create_metrics(sender, instance, created, **kwargs):
    """Auto create metrics according to template"""
    if created:
        instance.create_metrics()
