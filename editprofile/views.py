from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.userprofile)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user.userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
