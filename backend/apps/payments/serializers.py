from rest_framework import serializers


class InitializePaymentSerializer(serializers.Serializer):
    plan = serializers.CharField()
    provider = serializers.CharField(default="paystack")


class VerifyPaymentSerializer(serializers.Serializer):
    reference = serializers.CharField()