from rest_framework.permissions import BasePermission


class CanRunEligibility(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)