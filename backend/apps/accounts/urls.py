from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import HealthView, LoginView, ProfileView, RegisterView

urlpatterns = [
    path("health/", HealthView.as_view(), name="accounts-health"),
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", ProfileView.as_view(), name="accounts-profile"),
]
