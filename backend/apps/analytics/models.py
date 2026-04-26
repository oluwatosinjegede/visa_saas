from django.db import models


class AnalyticsEvent(models.Model):
    event_name = models.CharField(max_length=120)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class ConversionFunnel(models.Model):
    stage = models.CharField(max_length=120)
    count = models.PositiveIntegerField(default=0)


class ApplicationMetric(models.Model):
    country = models.CharField(max_length=120)
    total = models.PositiveIntegerField(default=0)


class RevenueMetric(models.Model):
    period = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=14, decimal_places=2)


class CountryTrend(models.Model):
    country = models.CharField(max_length=120)
    demand_score = models.FloatField(default=0)


class RefusalTrend(models.Model):
    reason = models.CharField(max_length=255)
    total = models.PositiveIntegerField(default=0)


class ConsultantPerformanceMetric(models.Model):
    consultant_id = models.PositiveIntegerField()
    success_rate = models.FloatField(default=0)


class LeadSourceMetric(models.Model):
    source = models.CharField(max_length=120)
    leads = models.PositiveIntegerField(default=0)
