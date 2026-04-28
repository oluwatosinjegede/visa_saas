from django.urls import path

from .views import CurrentSubscriptionView, HealthView, InitializePaymentView, SubscriptionPlansView, VerifyPaymentView

urlpatterns = [
    path("health/", HealthView.as_view(), name="payments-health"),
    path("plans/", SubscriptionPlansView.as_view(), name="payments-plans"),
    path("initialize/", InitializePaymentView.as_view(), name="payments-initialize"),
    path("verify/", VerifyPaymentView.as_view(), name="payments-verify"),
    path("current-subscription/", CurrentSubscriptionView.as_view(), name="payments-current-subscription"),
]
