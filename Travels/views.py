from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Travel
from .serializers import TravelSerializer

User = get_user_model()


class TravelView(APIView):
    serializer_class = TravelSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        travels = Travel.objects.all()
        travel_serializer = TravelSerializer(travels, many=True)
        return Response(data=travel_serializer.data, status=status.HTTP_200_OK)
