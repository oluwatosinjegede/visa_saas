from django.conf import settings
from django.db import models


class VisaCountry(models.Model):
    name = models.CharField(max_length=120, unique=True)
    iso_code = models.CharField(max_length=3, unique=True)


class VisaProgram(models.Model):
    country = models.ForeignKey(VisaCountry, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    minimum_score = models.PositiveSmallIntegerField(default=60)


class VisaRequirement(models.Model):
    visa_program = models.ForeignKey(VisaProgram, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    required = models.BooleanField(default=True)


class EligibilityQuestion(models.Model):
    visa_program = models.ForeignKey(VisaProgram, on_delete=models.CASCADE)
    question = models.TextField()
    requirement_code = models.CharField(max_length=100)


class EligibilityAnswer(models.Model):
    question = models.ForeignKey(EligibilityQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.TextField()


class EligibilityAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visa_program = models.ForeignKey(VisaProgram, on_delete=models.CASCADE)
    eligibility_status = models.CharField(max_length=30)
    score = models.PositiveSmallIntegerField(default=0)
    missing_requirements = models.JSONField(default=list)
    risk_flags = models.JSONField(default=list)
    recommended_next_steps = models.JSONField(default=list)


class VisaApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visa_program = models.ForeignKey(VisaProgram, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="draft")


class ApplicationStage(models.Model):
    visa_application = models.ForeignKey(VisaApplication, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    order = models.PositiveSmallIntegerField(default=1)


class ApplicationTimeline(models.Model):
    visa_application = models.ForeignKey(VisaApplication, on_delete=models.CASCADE)
    event = models.CharField(max_length=200)
    occurred_at = models.DateTimeField(auto_now_add=True)


class RiskFlag(models.Model):
    visa_application = models.ForeignKey(VisaApplication, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    detail = models.TextField(blank=True)


class RefusalAnalysis(models.Model):
    visa_application = models.ForeignKey(VisaApplication, on_delete=models.CASCADE)
    summary = models.TextField()
    reasons = models.JSONField(default=list)
