from rest_framework.permissions import BasePermission


class IsPaidUser(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request.user, "is_paid", False) or request.user.is_staff)