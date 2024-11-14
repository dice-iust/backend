from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserProfileUpdateSerializer
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

class UserProfileUpdateAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_classes=UserProfileUpdateSerializer
    def get(self, request):
        user_token = request.COOKIES.get("access_token")
        if not user_token:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        serializer = UserProfileUpdateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user_token = request.COOKIES.get("access_token")
        if not user_token:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
