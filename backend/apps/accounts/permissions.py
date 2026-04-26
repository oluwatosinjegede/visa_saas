from rest_framework.permissions import BasePermission
from .models import Role


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in {Role.SUPER_ADMIN, Role.PLATFORM_ADMIN})
