from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserProfileSerializer
from rest_framework.authentication import TokenAuthentication
from .models import UserProfile
class UserProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    seializer_class = UserProfileSerializer
    def get(self, request):
        users=UserProfile.objects.all()
        serializer = UserProfileSerializer(users,many=True)
        return Response(serializer.data)
    def put(self, request):
        serializer = UserProfileSerializer(request.user.userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
