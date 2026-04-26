from django.conf import settings
from django.db import models


class DocumentType(models.Model):
    name = models.CharField(max_length=120)


class Document(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    file = models.FileField(upload_to="documents/")
    is_private = models.BooleanField(default=True)


class DocumentChecklist(models.Model):
    name = models.CharField(max_length=120)


class DocumentChecklistItem(models.Model):
    checklist = models.ForeignKey(DocumentChecklist, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    required = models.BooleanField(default=True)


class DocumentReview(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default="pending")


class DocumentComment(models.Model):
    review = models.ForeignKey(DocumentReview, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
