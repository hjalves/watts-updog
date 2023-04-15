from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Home(models.Model):
    name = models.CharField()
    mqtt_topic = models.CharField("MQTT topic", max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "home"
        verbose_name_plural = "homes"

    def __str__(self):
        return self.name

    @property
    def full_mqtt_topic(self):
        return self.mqtt_topic

    def owners(self):
        return self.householdmembership_set.filter(
            relationship=HouseholdMembership.RELATIONSHIP_OWNER
        )


class HouseholdMembership(models.Model):
    RELATIONSHIP_OWNER = "owner"
    RELATIONSHIP_GUEST = "guest"
    RELATIONSHIP_CHOICES = (
        (RELATIONSHIP_OWNER, "Owner"),
        (RELATIONSHIP_GUEST, "Guest"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    relationship = models.CharField(
        choices=RELATIONSHIP_CHOICES, default=RELATIONSHIP_OWNER, max_length=5
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "household membership"
        verbose_name_plural = "household memberships"

    def __str__(self):
        return f"{self.user} on {self.home}"
