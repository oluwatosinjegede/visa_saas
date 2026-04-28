import httpx
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment, Subscription, SubscriptionPlan
from .serializers import InitializePaymentSerializer, SubscriptionPlanSerializer, VerifyPaymentSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({"module": "payments", "status": "ok"})


class SubscriptionPlansView(APIView):
    permission_classes = [IsAuthenticated]

    PLAN_CATALOG = {
        SubscriptionPlan.BASIC: {
            "amount_kobo": 1900,
            "description": "Ideal for individual applicants getting started.",
            "features": ["Checklist", "Basic scoring", "Single applicant"],
        },
        SubscriptionPlan.PREMIUM: {
            "amount_kobo": 4900,
            "description": "Best for serious applicants that need AI automation.",
            "features": ["AI scoring", "SOP + refusal analysis", "Priority support"],
        },
        SubscriptionPlan.CONSULTANT_PRO: {
            "amount_kobo": 9900,
            "description": "Built for teams, consultants, and advanced support.",
            "features": ["Consultant access", "Advanced analytics", "Team features"],
        },
    }

    def get(self, request):
        plans = [
            {
                "code": code,
                "name": SubscriptionPlan(code).label,
                "amount": detail["amount_kobo"] / 100,
                "amount_kobo": detail["amount_kobo"],
                "description": detail["description"],
                "features": detail["features"],
            }
            for code, detail in self.PLAN_CATALOG.items()
        ]
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response({"plans": serializer.data}, status=status.HTTP_200_OK)


class InitializePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    PLAN_TO_AMOUNT = SubscriptionPlansView.PLAN_CATALOG

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

        plan_pricing = self.PLAN_TO_AMOUNT.get(plan)
        if plan_pricing is None:
            return Response(
                {
                    "message": "Payment initialization failed",
                    "errors": {"plan": ["Selected plan is not supported."]},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_payment = Payment.objects.filter(user=request.user, plan=plan, status="pending").order_by("-id").first()
        if existing_payment:
            reference = existing_payment.reference
        else:
            reference = f"VP-{request.user.id}-{plan}-{Payment.objects.count() + 1}"
            Payment.objects.create(
                user=request.user,
                plan=plan,
                amount=plan_pricing["amount_kobo"] / 100,
                provider=provider,
                reference=reference,
                status="pending",
            )
        paystack_payload = {
            "email": request.user.email,
            "amount": plan_pricing["amount_kobo"],
            "reference": reference,
            "callback_url": settings.PAYSTACK_CALLBACK_URL,
            "currency": settings.PAYSTACK_CURRENCY,
            "metadata": {"user_id": request.user.id, "plan": plan},
        }
        paystack_headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = httpx.post(
                f"{settings.PAYSTACK_BASE_URL}/transaction/initialize",
                json=paystack_payload,
                headers=paystack_headers,
                timeout=20,
            )
            response.raise_for_status()
            response_data = response.json()
        except (httpx.HTTPError, ValueError):
            return Response(
                {
                    "message": "Payment initialization failed",
                    "errors": {"provider": ["Unable to initialize transaction with Paystack."]},
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        authorization_url = response_data.get("data", {}).get("authorization_url")
        if not authorization_url:
            return Response(
                {
                    "message": "Payment initialization failed",
                    "errors": {"provider": ["Paystack did not return an authorization URL."]},
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )


        return Response(
            {
                "message": "Payment initialized successfully",
                "authorization_url": authorization_url,
                "reference": reference,
                "plan": plan,
            },
            status=status.HTTP_200_OK,
        )


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = VerifyPaymentSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        reference = serializer.validated_data["reference"]

        payment = Payment.objects.filter(user=request.user, reference=reference).first()
        if not payment:
            return Response(
                {
                    "message": "Payment verification failed",
                    "errors": {"reference": ["Payment reference was not found."]},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        payment.status = "success"
        payment.save(update_fields=["status"])

        Subscription.objects.update_or_create(
            user=request.user,
            defaults={"plan": payment.plan, "active": True},
        )

        return Response(
            {"message": "Payment verified", "status": "success", "plan": SubscriptionPlan(payment.plan).label},
            status=status.HTTP_200_OK,
        )

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