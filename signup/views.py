from django.shortcuts import render
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserViewSerializer,
    EmailVerificationSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
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
from .generate import generate_access_token, generate_secure_token
import random
from django.core.mail import send_mail
from .models import EmailVerification
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import re
import uuid

User = get_user_model()


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        AllowAny,
    ]

    def get(self, request):
        content = {"message": "Hello!"}
        return Response(content)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Check if the user already exists
            if (
                User.objects.filter(
                    user_name=serializer.validated_data["user_name"]
                ).exists()
                and not User.objects.filter(
                    email=serializer.validated_data["email"]
                ).exists()
            ):
                return Response(
                    {"error": "This user_name already exists."},
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
                    {"error": "This user_name and email already exist."},
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
    permission_classes = [
        AllowAny,
    ]

    def get(self, request):
        photo_response = {
            "photo": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}login.jpg"
        }
        return Response(photo_response)

    def post(self, request):
        user_name = request.data.get("user_name", None)
        user_password = request.data.get("password", None)

        if not user_password:
            raise AuthenticationFailed("A password is needed.")

        if not user_name:
            raise AuthenticationFailed("A user_name is needed.")

        user_instance = authenticate(user_name=user_name, password=user_password)

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
    permission_classes = [
        AllowAny,
    ]

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
    permission_classes = [
        AllowAny,
    ]

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


class UserRegistrationAndVerificationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        AllowAny,
    ]

    def get(self, request):
        content = {
            "message": "Hello!",
        }
        return Response(content)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            if (
                User.objects.filter(
                    user_name=serializer.validated_data["user_name"]
                ).exists()
                and not User.objects.filter(
                    email=serializer.validated_data["email"]
                ).exists()
            ):
                return Response(
                    {"error": "This user_name already exists."},
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
                    {"error": "This user_name and email already exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            verification_code = str(random.randint(1000, 9999))
            if (
                not serializer.validated_data["password"]
                or len(serializer.validated_data["password"]) < 6
            ):
                raise serializers.ValidationError(
                    "Password must be at least 6 characters"
                )
            if not re.search(r"[A-Za-z]", serializer.validated_data["password"]):
                return Response("Password must contain at least one letter")
            if not re.search(r"[0-9]", serializer.validated_data["password"]):
                return Response("Password must contain at least one number")
            token = generate_secure_token()
            EmailVerification.objects.create(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["user_name"],
                password=serializer.validated_data["password"],
                verification_code=verification_code,
                token=token,
            )
            send_mail(
                subject="Your Verification Code",
                message=f"Your verification code is: {verification_code}",
                from_email="your_email@example.com",
                recipient_list=[serializer.validated_data["email"]],
            )
            context = {"email": serializer.validated_data["email"], "token": token}
            return Response(context)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    serializer = EmailVerificationSerializer
    permission_classes = [AllowAny]
    authentication_classes = [
        TokenAuthentication,
    ]

    def get(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        verification = EmailVerification.objects.filter(token=token).last()
        if not verification:
            return Response(
                {"error": "No verification record found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "email": verification.email,
                "photo": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}veri2.jpg",
            }
        )

    def post(self, request, *args, **kwargs):
        email_serializer = self.serializer(data=request.data)
        if email_serializer.is_valid():
            token = request.headers.get("Authorization")
            verification_send_code = email_serializer.validated_data[
                "verification_code"
            ]
            verification = EmailVerification.objects.filter(token=token).last()
            if not verification:
                return Response(
                    {"error": "No verification record found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if verification.verification_code == verification_send_code:
                new_user = User.objects.create(
                    user_name=verification.username,
                    email=verification.email,
                    password=verification.password,
                )
                new_user.set_password(verification.password)
                new_user.save()
                access_token = generate_access_token(new_user)
                data = {"access_token": access_token}
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(
                    key="access_token", value=access_token, httponly=True
                )
                verification.delete()
                return response
            verification.delete()
            return Response(
                {"error": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# forgot_password:
class ForgotPasswordView(APIView):
    permission_classes = ((AllowAny),)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = request.build_absolute_uri(
                reverse(
                    "password-reset-confirm", kwargs={"uidb64": uid, "token": token}
                )
            )

            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_link}",
                from_email="triiptide@gmail.com",
                recipient_list=[email],
            )
            return Response(
                {"message": "Password reset link sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = ((AllowAny),)
    serializer_class = PasswordResetSerializer

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)

                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response(
                        {"error": "Invalid or expired token."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                newPassword = serializer.validated_data["newPassword"]
                user.set_password(newPassword)
                user.save()
                return Response(
                    {"message": "Password reset successful."}, status=status.HTTP_200_OK
                )
            except (User.DoesNotExist, ValueError):
                return Response(
                    {"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
