from django.conf import settings
from django.db import models


class PromptTemplate(models.Model):
    key = models.CharField(max_length=120, unique=True)
    prompt = models.TextField()


class AIConversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class AIMessage(models.Model):
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class AIAnalysisResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=100)
    output = models.JSONField(default=dict)
    disclaimer = models.TextField()
