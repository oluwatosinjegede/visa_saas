from django.urls import path

from .views import AdminOverviewView, AdminUsersView, HealthView

urlpatterns = [
    path('health/', HealthView.as_view(), name='admin_portal-health'),
    path('overview/', AdminOverviewView.as_view(), name='admin_portal-overview'),
    path('users/', AdminUsersView.as_view(), name='admin_portal-users'),
]
