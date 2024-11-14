from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Travel
from .serializers import TravelSerializer
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

class TravelView(APIView):
    serializer_class = TravelSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        travels = Travel.objects.all()
        travel_serializer = TravelSerializer(travels, many=True)
        return Response(data=travel_serializer.data, status=status.HTTP_200_OK)

class SingleTravelView(APIView):
    serializer_class = TravelSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            travel_get = Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        travel_serializer = TravelSerializer(travel_get)
        return Response(data=travel_serializer.data, status=status.HTTP_200_OK)

