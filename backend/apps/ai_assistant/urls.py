from django.urls import path

from .views import HealthView, RefusalAnalysisView, SOPGeneratorView

urlpatterns = [
    path("health/", HealthView.as_view(), name="ai_assistant-health"),
    path("sop-generator/", SOPGeneratorView.as_view(), name="ai-sop-generator"),
    path("refusal-analysis/", RefusalAnalysisView.as_view(), name="ai-refusal-analysis"),
]
