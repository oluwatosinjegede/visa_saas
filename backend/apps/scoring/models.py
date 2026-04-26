from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class ApplicantProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    country = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100)
    work_experience = models.IntegerField(help_text="Years of experience")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} Profile"


class SOPSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    sop_text = models.TextField()
    result = models.JSONField(default=dict, blank=True)
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOP - {self.user}"