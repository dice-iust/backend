from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
from models import *
from serializers import TravelSerializers
User = get_user_model()

class TravelView(APIView):
    serializer_class = TravelSerializer
    permission_classes=[AllowAny]
    
    def get(self,request):
        travels=TravelSerializers(many=True)
        return Response(data=travels.data)