from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/visa/", include("apps.visa.urls")),
    path("api/v1/documents/", include("apps.documents.urls")),
    path("api/v1/ai/", include("apps.ai_assistant.urls")),
    path("api/v1/relocation/", include("apps.relocation.urls")),
    path("api/v1/study/", include("apps.study.urls")),
    path("api/v1/analytics/", include("apps.analytics.urls")),
    path("api/v1/payments/", include("apps.payments.urls")),
    path("api/v1/admin/", include("apps.admin_portal.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/compliance/", include("apps.compliance.urls")),
]