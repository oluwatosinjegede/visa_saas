from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment, Subscription, SubscriptionPlan
from .serializers import InitializePaymentSerializer, VerifyPaymentSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({"module": "payments", "status": "ok"})


class InitializePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    PLAN_TO_AMOUNT = {
        "Starter": 1900,
        "Pro": 4900,
        "Premium": 9900,
    }

    def post(self, request):
        serializer = InitializePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = serializer.validated_data["plan"]
        provider = serializer.validated_data["provider"].lower()

        if provider != "paystack":
            return Response(
                {
                    "message": "Payment initialization failed",
                    "errors": {"provider": ["Only paystack is currently supported."]},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        amount = self.PLAN_TO_AMOUNT.get(plan)
        if amount is None:
            return Response(
                {
                    "message": "Payment initialization failed",
                    "errors": {"plan": ["Selected plan is not supported."]},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reference = f"VP-{request.user.id}-{plan.upper()}"
        Payment.objects.create(user=request.user, amount=amount / 100, provider=provider, status="pending")

        return Response(
            {
                "message": "Payment initialized successfully",
                "authorization_url": f"https://paystack.com/pay/{reference}",
                "reference": reference,
            },
            status=status.HTTP_200_OK,
        )


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = VerifyPaymentSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        Subscription.objects.update_or_create(
            user=request.user,
            defaults={"plan": SubscriptionPlan.BASIC, "active": True},
        )

        return Response({"message": "Payment verified", "status": "success"}, status=status.HTTP_200_OK)


class CurrentSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = Subscription.objects.filter(user=request.user, active=True).first()
        if not subscription:
            return Response({"plan": "Free", "active": False}, status=status.HTTP_200_OK)

        return Response(
            {
                "plan": subscription.get_plan_display(),
                "active": subscription.active,
            },
            status=status.HTTP_200_OK,
        )