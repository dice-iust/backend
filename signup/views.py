from django.shortcuts import render
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserViewSerializer,
)
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from .generate import generate_access_token

User = get_user_model()


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {"message": "Hello!"}
        return Response(content)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Check if the user already exists
            if User.objects.filter(
                user_name=serializer.validated_data["user_name"]
            ).exists() and not User.objects.filter(email=serializer.validated_data["email"]).exists():
                return Response(
                    {"error": "This username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if (
                User.objects.filter(email=serializer.validated_data["email"]).exists()
                and not User.objects.filter(
                    user_name=serializer.validated_data["user_name"]
                ).exists()
            ):
                return Response(
                    {"error": "This email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            if (
                User.objects.filter(email=serializer.validated_data["email"]).exists()
                and User.objects.filter(
                    user_name=serializer.validated_data["user_name"]
                ).exists()
            ):
                return Response(
                    {"error": "This username and email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_user = serializer.save()
            if new_user:
                access_token = generate_access_token(new_user)
                data = {"access_token": access_token}
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(
                    key="access_token", value=access_token, httponly=True
                )
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        user_name = request.data.get("user_name", None)
        user_password = request.data.get("password", None)

        if not user_password:
            raise AuthenticationFailed("A user password is needed.")

        if not user_name:
            raise AuthenticationFailed("An user user name is needed.")

        user_instance = authenticate(username=user_name, password=user_password)

        if not user_instance:
            raise AuthenticationFailed("User not found.")

        if user_instance.is_active:
            user_access_token = generate_access_token(user_instance)
            response = Response()
            response.set_cookie(
                key="access_token", value=user_access_token, httponly=True
            )
            response.data = {"access_token": user_access_token}
            return response
        return Response({"message": "Something went wrong."})


class UserViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get("access_token")

        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        user_serializer = UserViewSerializer(user)
        return Response(user_serializer.data)


class UserLogoutViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get("access_token", None)
        if user_token:
            response = Response()
            response.delete_cookie("access_token")
            response.data = {"message": "Logged out successfully."}
            return response
        response = Response()
        response.data = {"message": "User is already logged out."}
        return response
