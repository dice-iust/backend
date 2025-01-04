from django.shortcuts import render
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserViewSerializer,
    EmailVerificationSerializer,
    BlacklistedToken,
)
from rest_framework.generics import GenericAPIView
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
from .serializers import PasswordResetRequestSerializer, PasswordResetVerifySerializer
from .models import PasswordResetRequest
from datetime import datetime, timezone


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
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")
        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            raise AuthenticationFailed("User not found.")

        BlacklistedToken.objects.create(
            token=user_token, blacklisted_at=datetime.now(timezone.utc)
        )
        response = Response({"message": "Logged out successfully."})
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
                subject="Verify Your Account - Your Verification Code",
                message=f"""
                    Hello {serializer.validated_data["user_name"]},

                    Thank you for signing up! To complete your registration, please use the following verification code:

                    {verification_code}

                    Please enter this code on the verification page to activate your account.

                    If you did not request this email, please ignore it.

                    Best regards,  
                    The TripTide Team
                """,
                from_email="triiptide@gmail.com",
                recipient_list=[serializer.validated_data["email"]],
                html_message=f"""
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f9f9f9;
                                }}
                                .email-container {{
                                    max-width: 600px;
                                    margin: 20px auto;
                                    background: #ffffff;
                                    border: 1px solid #dddddd;
                                    border-radius: 8px;
                                    overflow: hidden;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                }}
                                .header {{
                                    background-color: #22487a;
                                    color: white;
                                    padding: 20px;
                                    text-align: center;
                                }}
                                .content {{
                                    padding: 20px;
                                    color: #333333;
                                    line-height: 1.6;
                                }}
                                .verification-code {{
                                    font-size: 24px;
                                    font-weight: bold;
                                    color: #22487a;
                                    text-align: center;
                                    margin: 20px 0;
                                }}
                                .footer {{
                                    text-align: center;
                                    padding: 10px;
                                    font-size: 12px;
                                    color: #888888;
                                    background-color: #f9f9f9;
                                    border-top: 1px solid #dddddd;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <h1>Verify Your Account</h1>
                                </div>
                                <div class="content">
                                    <p>Hello <strong>{serializer.validated_data["user_name"]}</strong>,</p>
                                    <p>
                                        Thank you for signing up! To complete your registration, please use the following 
                                        verification code:
                                    </p>
                                    <div class="verification-code">
                                        {verification_code}
                                    </div>
                                    <p>
                                        Please enter this code on the verification page to activate your account.
                                    </p>
                                    <p>
                                        If you did not request this email, please ignore it.
                                    </p>
                                    <p>Best regards,</p>
                                </div>
                                <div class="footer">
                                    <p>&copy; TripTide Team</p>
                                </div>
                            </div>
                        </body>
                    </html>
                """,
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
                "photo": f"https://triptide.liara.run{settings.MEDIA_URL}veri2.jpg",
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
                    {"success": False},
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
                user_access_token = generate_access_token(new_user)
                response = Response()
                response.set_cookie(
                    key="access_token", value=user_access_token, httponly=True
                )
                response.data = {"access_token": user_access_token, "success": True}
                verification.delete()
                return response
            verification.delete()
            return Response(
                {"error": "Invalid verification code.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"seccess": False}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist.", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            reset_code = PasswordResetRequest.generate_reset_code()
            reset_request = PasswordResetRequest.objects.create(
                user=user, reset_code=reset_code
            )
            send_mail(
                subject="Password Reset Code",
                message=f"Your password reset code is: {reset_code}",
                from_email="from@example.com",
                recipient_list=[email],
                fail_silently=False,
                html_message=f"""
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f9f9f9;
                                }}
                                .email-container {{
                                    max-width: 600px;
                                    margin: 20px auto;
                                    background: #ffffff;
                                    border: 1px solid #dddddd;
                                    border-radius: 8px;
                                    overflow: hidden;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                }}
                                .header {{
                                    background-color: #22487a;
                                    color: white;
                                    padding: 20px;
                                    text-align: center;
                                }}
                                .content {{
                                    padding: 20px;
                                    color: #333333;
                                    line-height: 1.6;
                                }}
                                .reset-code {{
                                    font-size: 24px;
                                    font-weight: bold;
                                    color: #22487a;
                                    text-align: center;
                                    margin: 20px 0;
                                }}
                                .footer {{
                                    text-align: center;
                                    padding: 10px;
                                    font-size: 12px;
                                    color: #888888;
                                    background-color: #f9f9f9;
                                    border-top: 1px solid #dddddd;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <h1>Password Reset Request</h1>
                                </div>
                                <div class="content">
                                    <p>Hello,</p>
                                    <p>
                                        We received a request to reset your password. Please use the following code to reset your password:
                                    </p>
                                    <div class="reset-code">
                                        {reset_code}
                                    </div>
                                    <p>
                                        If you didn’t request this, you can safely ignore this email.
                                    </p>
                                    <p>Best regards,</p>
                                </div>
                                <div class="footer">
                                    <p>&copy; TripTide Team</p>
                                </div>
                            </div>
                        </body>
                    </html>
                """,
            )

            return Response(
                {
                    "message": "A reset code has been sent to your email.",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"errors": serializer.errors, "success": False},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email", None)

        if not email:
            return Response(
                {"error": "Email parameter is required.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
            reset_request = PasswordResetRequest.objects.filter(
                user=user, is_verified=False
            ).first()

            if reset_request:
                return Response(
                    {
                        "message": "Password reset request is pending.",
                        "reset_code": reset_request.reset_code,
                        "status": "pending",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "No pending password reset request found.",
                        "status": "completed or not requested",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )

        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetVerifyAPIView(GenericAPIView):
    serializer_class = PasswordResetVerifySerializer

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email", None)

        if not email:
            return Response(
                {"error": "Email parameter is required.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
            reset_request = PasswordResetRequest.objects.filter(
                user=user, is_verified=False
            ).first()

            if reset_request:
                return Response(
                    {
                        "message": "Password reset request is pending.",
                        "reset_code": reset_request.reset_code,
                        "status": "pending",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "No pending password reset request found.",
                        "status": "completed or not requested",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )

        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            reset_code = serializer.validated_data["reset_code"]
            new_password = serializer.validated_data["new_password"]

            try:
                reset_request = PasswordResetRequest.objects.get(
                    user__email=email, reset_code=reset_code, is_verified=False
                )
            except PasswordResetRequest.DoesNotExist:
                return Response(
                    {"error": "Invalid or expired reset code.", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = reset_request.user
            user.set_password(new_password)
            user.save()

            reset_request.is_verified = True
            reset_request.save()

            return Response(
                {"message": "Password has been successfully updated.", "success": True},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"errors": serializer.errors, "success": False},
            status=status.HTTP_400_BAD_REQUEST,
        )
