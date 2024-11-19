from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserProfileUpdateSerializer
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from signup.generate import generate_access_token
class UserProfileUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_classes = UserProfileUpdateSerializer

    def get(self, request):
        user_token = request.COOKIES.get("access_token")
        if not user_token:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        default_data = {
            "currentPassword": None,
            "newPassword": None,
            "confirmPassword": None
        }
        serializer = UserProfileUpdateSerializer(user)
        response_data = {**serializer.data, **default_data}
        return Response(response_data, status=status.HTTP_200_OK)

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

        serializer = UserProfileUpdateSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            access_token = generate_access_token(user)
            data = {"access_token": access_token}

            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.set_cookie(key="access_token", value=access_token, httponly=True)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
