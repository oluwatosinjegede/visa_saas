from django.urls import path
from .views import HealthView, LoginView, ProfileView, RegisterView

urlpatterns = [
    path("health/", HealthView.as_view(), name="accounts-health"),
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("profile/", ProfileView.as_view(), name="accounts-profile"),
]
