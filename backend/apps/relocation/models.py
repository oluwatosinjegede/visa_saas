from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=120, unique=True)


class RelocationProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination_country = models.CharField(max_length=120)
    job_readiness_score = models.PositiveSmallIntegerField(default=0)


class WorkExperience(models.Model):
    profile = models.ForeignKey(RelocationProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    years = models.PositiveSmallIntegerField(default=0)


class CandidateSkill(models.Model):
    profile = models.ForeignKey(RelocationProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=40, default="intermediate")


class Employer(models.Model):
    name = models.CharField(max_length=255)
    supports_sponsorship = models.BooleanField(default=False)


class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class JobPosting(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    destination_country = models.CharField(max_length=120)


class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="submitted")


class JobMatchScore(models.Model):
    profile = models.ForeignKey(RelocationProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    match_score = models.PositiveSmallIntegerField(default=0)
    missing_skills = models.JSONField(default=list)


class RelocationChecklist(models.Model):
    profile = models.ForeignKey(RelocationProfile, on_delete=models.CASCADE)
    items = models.JSONField(default=list)


class WorkPermitPathway(models.Model):
    country = models.CharField(max_length=120)
    name = models.CharField(max_length=200)
