from typing import NamedTuple

from metrics.models import Metric


class MetricDecl(NamedTuple):
    type: str
    data_type: str
    mqtt_topic: str


emi_metrics = [
    MetricDecl(Metric.METRIC_POWER, Metric.DATA_TYPE_FLOAT, "power"),
    MetricDecl(Metric.METRIC_ENERGY_TOTAL, Metric.DATA_TYPE_FLOAT, "energy/total"),
    MetricDecl(Metric.METRIC_ENERGY_CHEIAS, Metric.DATA_TYPE_FLOAT, "energy/cheias"),
    MetricDecl(Metric.METRIC_ENERGY_PONTA, Metric.DATA_TYPE_FLOAT, "energy/ponta"),
    MetricDecl(Metric.METRIC_ENERGY_VAZIO, Metric.DATA_TYPE_FLOAT, "energy/vazio"),
    MetricDecl(Metric.METRIC_TARIFF, Metric.DATA_TYPE_STRING, "tariff"),
    MetricDecl(Metric.METRIC_VOLTAGE, Metric.DATA_TYPE_FLOAT, "voltage"),
    MetricDecl(Metric.METRIC_FREQUENCY, Metric.DATA_TYPE_FLOAT, "frequency"),
    MetricDecl(Metric.METRIC_CURRENT, Metric.DATA_TYPE_FLOAT, "current"),
]
