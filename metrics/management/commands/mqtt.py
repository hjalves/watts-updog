import logging
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from paho.mqtt import subscribe

from metrics.models import Metric, FloatMeasurement, StringMeasurement

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Subscribe for MQTT events and save measurements to database"

    def __init__(self):
        super().__init__()
        self.topic_cache = {}
        self.refresh_cache_every = 120
        self.last_refresh = 0

    def add_arguments(self, parser):
        parser.add_argument(
            "--hostname",
            default=settings.MQTT_HOST,
            help="address of the mqtt broker",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=settings.MQTT_PORT,
            help="port of the mqtt broker",
        )
        parser.add_argument(
            "--qos",
            type=int,
            default=2,
            help="the qos used when subscribing",
        )
        parser.add_argument(
            "--topics",
            default=["#"],
            nargs="*",
            help="topics to subscribe to",
        )
        parser.add_argument(
            "--cache",
            type=int,
            default=self.refresh_cache_every,
            metavar="SEC",
            help="refresh cache every x seconds",
        )

    def refresh_cache(self):
        logger.debug("Reloading topic->metric data")
        for metric in Metric.objects.all():
            mqtt_topic = metric.full_mqtt_topic
            self.topic_cache[mqtt_topic] = metric.id, metric.data_type
        self.last_refresh = time.time()
        logger.debug("Topics: %s", ", ".join(self.topic_cache.keys()))

    def handle(self, *args, **options):
        self.refresh_cache()
        logger.info(
            "Will connect to MQTT %(hostname)s:%(port)s (qos=%(qos)s), topics=%(topics)s",
            options,
        )
        subscribe.callback(
            self.handle_mqtt_message,
            topics=options["topics"],
            qos=options["qos"],
            hostname=options["hostname"],
            port=options["port"],
        )

    def handle_mqtt_message(self, client, userdata, message):
        if message.topic in self.topic_cache:
            logger.debug("Saving: topic=%r, payload=%r", message.topic, message.payload)
            metric_id, data_type = self.topic_cache[message.topic]
            value = message.payload.decode()
            try:
                self.create_measurement(metric_id, data_type, value)
            except Exception:
                logger.exception(
                    "Could not add measurement: topic=%r, metric_id=%r, value=%r",
                    message.topic,
                    metric_id,
                    message.payload,
                )
        else:
            logger.debug("Ignoring: topic=%r, payload=%r", message.topic, message.payload)

        if time.time() - self.last_refresh > self.refresh_cache_every:
            self.refresh_cache()

    def create_measurement(self, metric_id, data_type, value):
        logger.info(
            "Creating measurement: metric_id=%r, data_type=%r, value=%r",
            metric_id,
            data_type,
            value,
        )
        now = timezone.now()
        match data_type:
            case Metric.DATA_TYPE_FLOAT:
                return FloatMeasurement.objects.create(
                    time=now, metric_id=metric_id, value=float(value)
                )
            case Metric.DATA_TYPE_STRING:
                return StringMeasurement.objects.create(
                    time=now, metric_id=metric_id, value=str(value)
                )
