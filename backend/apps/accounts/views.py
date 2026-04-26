from rest_framework.views import APIView
from rest_framework.response import Response


class HealthView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({"module": "accounts", "status": "ok"})
