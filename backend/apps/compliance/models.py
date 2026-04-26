from django.db import models


class PolicyDocument(models.Model):
    policy_type = models.CharField(max_length=120)
    content = models.TextField()
    version = models.CharField(max_length=40)
    effective_date = models.DateField()
