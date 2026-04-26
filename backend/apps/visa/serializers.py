from rest_framework import serializers
from .models import EligibilityAssessment, VisaProgram


class VisaProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaProgram
        fields = "__all__"


class EligibilityAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityAssessment
        fields = "__all__"