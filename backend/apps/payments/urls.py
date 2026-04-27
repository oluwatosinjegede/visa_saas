from django.urls import path

from .views import CurrentSubscriptionView, HealthView, InitializePaymentView, VerifyPaymentView

urlpatterns = [
    path("health/", HealthView.as_view(), name="payments-health"),
    path("initialize/", InitializePaymentView.as_view(), name="payments-initialize"),
    path("verify/", VerifyPaymentView.as_view(), name="payments-verify"),
    path("current-subscription/", CurrentSubscriptionView.as_view(), name="payments-current-subscription"),
]
