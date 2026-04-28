from rest_framework import serializers

from .models import SubscriptionPlan


class SubscriptionPlanSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    amount_kobo = serializers.IntegerField()
    description = serializers.CharField()
    features = serializers.ListField(child=serializers.CharField())


class InitializePaymentSerializer(serializers.Serializer):
    plan = serializers.ChoiceField(choices=SubscriptionPlan.values)
    provider = serializers.CharField(default="paystack")


class VerifyPaymentSerializer(serializers.Serializer):
    reference = serializers.CharField()