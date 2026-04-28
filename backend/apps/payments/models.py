from django.conf import settings
from django.db import models


class SubscriptionPlan(models.TextChoices):
    FREE = "FREE", "Free"
    BASIC = "BASIC", "Basic"
    PREMIUM = "PREMIUM", "Premium"
    CONSULTANT_PRO = "CONSULTANT_PRO", "Consultant Pro"
    SCHOOL_PARTNER = "SCHOOL_PARTNER", "School Partner"
    EMPLOYER_PARTNER = "EMPLOYER_PARTNER", "Employer Partner"
    ENTERPRISE = "ENTERPRISE", "Enterprise"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=40, choices=SubscriptionPlan.choices, default=SubscriptionPlan.FREE)
    active = models.BooleanField(default=True)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=40, choices=SubscriptionPlan.choices, default=SubscriptionPlan.FREE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=30)
    reference = models.CharField(max_length=120, unique=True)
    status = models.CharField(max_length=30, default="pending")
