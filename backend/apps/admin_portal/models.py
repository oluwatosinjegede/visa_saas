from django.db import models


class AdminActionLog(models.Model):
    actor_id = models.PositiveIntegerField()
    action = models.CharField(max_length=200)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
