from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import include, path


def root_status(request):
    return JsonResponse({
        "service": "visa-saas",
        "status": "ok",
        "api_version": "v1",
    })


def favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    path("", root_status, name="root-status"),
    path("favicon.ico", favicon, name="favicon"),

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
    path("api/v1/scoring/", include("apps.scoring.urls")),
]