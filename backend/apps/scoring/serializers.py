from rest_framework import serializers
from .models import ApplicantProfile, SOPSubmission


class ApplicantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantProfile
        fields = ['age', 'education', 'ielts', 'refusals', 'funds']


class SOPUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SOPResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOPSubmission
        fields = ['id', 'score', 'feedback', 'created_at']