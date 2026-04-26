
from django.urls import path
from .views import (
    CreateOrUpdateProfileView,
    SOPUploadView,
    UserResultsView,
)

urlpatterns = [
    path("profile/", CreateOrUpdateProfileView.as_view()),
    path("upload/", SOPUploadView.as_view()),
    path("results/", UserResultsView.as_view()),
]