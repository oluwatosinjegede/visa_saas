from rest_framework import serializers

class SOPGeneratorSerializer(serializers.Serializer):
    background = serializers.CharField()
    education = serializers.CharField()
    work_history = serializers.CharField()
    goal = serializers.CharField()
    country_choice = serializers.CharField()
    financial_sponsor = serializers.CharField()
    home_ties = serializers.CharField()
    career_plan = serializers.CharField()


class RefusalAnalysisSerializer(serializers.Serializer):
    refusal_text = serializers.CharField()

