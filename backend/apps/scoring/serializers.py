from rest_framework import serializers
from .models import ApplicantProfile, SOPSubmission


class ApplicantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantProfile
        fields = ['age', 'country', 'education_level', 'work_experience']


class SOPUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SOPResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOPSubmission
        fields = ['id', 'score', 'feedback', 'result', 'created_at']