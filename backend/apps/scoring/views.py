from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ApplicantProfile, SOPSubmission, VisaAssessmentSubmission
from .permissions import IsPaidUser
from .serializers import (
    ApplicantProfileSerializer,
    SOPResultSerializer,
    VisaAssessmentQuestionnaireSerializer,
    VisaAssessmentResultSerializer,
    SOPUploadSerializer,
)
from .services import analyze_application, assess_questionnaire
from .utils import extract_text_from_file


class CreateOrUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplicantProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile, _ = ApplicantProfile.objects.update_or_create(
            user=request.user,
            defaults=serializer.validated_data,
        )

        return Response(
            {
                "message": "Profile saved successfully",
                "data": ApplicantProfileSerializer(profile).data,
            },
            status=status.HTTP_200_OK,
        )


class SOPUploadView(APIView):
    permission_classes = [IsAuthenticated, IsPaidUser]

    def post(self, request):
        serializer = SOPUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        try:
            sop_text = extract_text_from_file(file)
        except Exception:
            return Response(
                {"message": "SOP upload failed", "errors": {"file": ["Failed to read file"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = ApplicantProfile.objects.filter(user=request.user).first()

        if not profile:
            return Response(
                {"message": "SOP upload failed", "errors": {"profile": ["Please complete your profile first"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = analyze_application(profile, sop_text)
        except Exception:
            return Response(
                {"error": "AI analysis failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        submission = SOPSubmission.objects.create(
            user=request.user,
            sop_text=sop_text,
            result=result,
            score=result.get("score") if isinstance(result, dict) else None,
        )

        return Response(
            {
                "message": "Analysis complete",
                "data": SOPResultSerializer(submission).data
            },
            status=status.HTTP_200_OK,
        )


class UserResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = SOPSubmission.objects.filter(user=request.user).order_by("-created_at")

        serializer = SOPResultSerializer(results, many=True)

        return Response(
            {
                "count": results.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class VisaAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VisaAssessmentQuestionnaireSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        questionnaire = serializer.validated_data
        assessment_result = assess_questionnaire(questionnaire)

        submission = VisaAssessmentSubmission.objects.create(
            user=request.user,
            questionnaire=questionnaire,
            score=assessment_result["score"],
            approval_probability=assessment_result["approval_probability"],
            refusal_risk_level=assessment_result["refusal_risk_level"],
            refusal_risks=assessment_result["refusal_risks"],
            recommendations=assessment_result["recommendations"],
            ai_refusal_prediction=assessment_result["ai_refusal_prediction"],
        )

        return Response(
            {
                "message": "Visa assessment complete",
                "data": VisaAssessmentResultSerializer(submission).data,
            },
            status=status.HTTP_200_OK,
        )


class VisaAssessmentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        submissions = VisaAssessmentSubmission.objects.filter(user=request.user).order_by("-created_at")
        serializer = VisaAssessmentResultSerializer(submissions, many=True)

        return Response(
            {
                "count": submissions.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )