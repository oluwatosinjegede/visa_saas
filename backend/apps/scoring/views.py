from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsPaidUser
from .models import ApplicantProfile, SOPSubmission
from .serializers import (
    ApplicantProfileSerializer,
    SOPUploadSerializer,
    SOPResultSerializer
)
from .utils import extract_text_from_file
from .services import analyze_application


# 🔹 CREATE OR UPDATE PROFILE
class CreateOrUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplicantProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile, _ = ApplicantProfile.objects.update_or_create(
            user=request.user,
            defaults=serializer.validated_data
        )

        return Response(
            {
                "message": "Profile saved successfully",
                "data": ApplicantProfileSerializer(profile).data
            },
            status=status.HTTP_200_OK
        )


# 🔹 SOP UPLOAD + AI ANALYSIS
class SOPUploadView(APIView):
    permission_classes = [IsAuthenticated, IsPaidUser]

    def post(self, request):
        serializer = SOPUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        # Extract text safely
        try:
            sop_text = extract_text_from_file(file)
        except Exception as e:
            return Response(
                {"message": "SOP upload failed", "errors": {"file": ["Failed to read file"]}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user profile
        profile = ApplicantProfile.objects.filter(user=request.user).first()

        if not profile:
            return Response(
                {"message": "SOP upload failed", "errors": {"profile": ["Please complete your profile first"]}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # AI ANALYSIS
        try:
            result = analyze_application(profile, sop_text)
        except Exception as e:
            return Response(
                {"error": "AI analysis failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save submission
        submission = SOPSubmission.objects.create(
            user=request.user,
            sop_text=sop_text,
            result=result,
            score=result.get("score") if isinstance(result, dict) else None
        )

        return Response(
            {
                "message": "Analysis complete",
                "data": SOPResultSerializer(submission).data
            },
            status=status.HTTP_200_OK
        )


# GET USER RESULTS
class UserResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = SOPSubmission.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = SOPResultSerializer(results, many=True)

        return Response(
            {
                "count": results.count(),
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )