from django.urls import path

from .views import (
    CreateOrUpdateProfileView,
    SOPUploadView,
    UserResultsView,
    VisaAssessmentHistoryView,
    VisaAssessmentView,
)

urlpatterns = [
    path("profile/", CreateOrUpdateProfileView.as_view()),
    path("upload/", SOPUploadView.as_view()),
    path("results/", UserResultsView.as_view()),
    path("assessment/", VisaAssessmentView.as_view()),
    path("assessment/history/", VisaAssessmentHistoryView.as_view()),
]