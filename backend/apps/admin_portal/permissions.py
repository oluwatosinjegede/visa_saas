from rest_framework.permissions import BasePermission

from apps.accounts.models import Role

class IsAdminPortalUser(BasePermission):
    message = 'Admin role required.'

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role in {Role.SUPER_ADMIN, Role.PLATFORM_ADMIN}
        )
