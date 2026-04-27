from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User

from .permissions import IsAdminPortalUser
from .serializers import AdminUserCreateSerializer, AdminUserSerializer



class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'module': 'admin_portal', 'status': 'ok'})


class AdminOverviewView(APIView):
    permission_classes = [IsAdminPortalUser]

    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        role_breakdown = list(User.objects.values('role').annotate(total=Count('id')).order_by('-total', 'role'))
        recent_users = AdminUserSerializer(User.objects.order_by('-date_joined')[:5], many=True).data

        return Response(
            {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': max(total_users - active_users, 0),
                'role_breakdown': role_breakdown,
                'recent_users': recent_users,
            }
        )


class AdminUsersView(APIView):
    permission_classes = [IsAdminPortalUser]

    def get(self, request):
        query = (request.query_params.get('q') or '').strip()
        role = (request.query_params.get('role') or '').strip()

        users = User.objects.select_related('userprofile').order_by('-date_joined')
        if query:
            users = users.filter(
                Q(email__icontains=query)
                | Q(userprofile__full_name__icontains=query)
                | Q(username__icontains=query)
            )
        if role:
            users = users.filter(role=role)

        return Response({'results': AdminUserSerializer(users[:50], many=True).data, 'count': users.count()})

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = AdminUserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
