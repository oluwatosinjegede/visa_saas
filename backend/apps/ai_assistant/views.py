from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RefusalAnalysisSerializer, SOPGeneratorSerializer
from .services import AIHealthService


class HealthView(APIView):
    def get(self, request):
        return Response({"module": "ai_assistant", "status": "ok", "ai": AIHealthService.status()})
    


class SOPGeneratorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SOPGeneratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        sop = (
            f"I am applying to {data['country_choice']} for {data['goal']}. "
            f"My background: {data['background']}. Education: {data['education']}. "
            f"Experience: {data['work_history']}. Sponsored by: {data['financial_sponsor']}. "
            f"Home ties: {data['home_ties']}. Career plan: {data['career_plan']}."
        )

        return Response(
            {
                "message": "SOP generated successfully",
                "data": {"sop": sop},
            },
            status=status.HTTP_200_OK,
        )


class RefusalAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RefusalAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refusal_text = serializer.validated_data["refusal_text"].strip()
        summary = refusal_text[:300]

        return Response(
            {
                "message": "Refusal analysis complete",
                "data": {
                    "summary": summary,
                    "recommendation": "Address financial evidence, purpose clarity, and home-country ties before reapplying.",
                },
            },
            status=status.HTTP_200_OK,
        )
