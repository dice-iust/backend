from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date
import re

from rest_framework.exceptions import ValidationError

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import *
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100, min_length=6, style={"input_type": "password"}
    )
    confirmPassword = serializers.CharField(max_length=100, min_length=6, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["user_name", "email", "password", "confirmPassword"]

    # def create(self, validated_data):
    #     user_password = validated_data.pop("password")
    #     validated_data.pop("confirmPassword")
    #     if not user_password or len(user_password) < 6:
    #         raise serializers.ValidationError("Password must be at least 6 characters")
    #     if not re.search(r"[A-Za-z]", user_password):
    #         raise serializers.ValidationError(
    #             "Password must contain at least one letter"
    #         )
    #     if not re.search(r"[0-9]", user_password):
    #         raise serializers.ValidationError(
    #             "Password must contain at least one number"
    #         )
    #     user = User(**validated_data)
    #     user.set_password(user_password)
    #     user.save()
    #     return user

    def validate(self, data):
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        if not confirmPassword:
            raise serializers.ValidationError("Please enter confirm password")
        if not password:
            raise serializers.ValidationError("Please enter password")
        if password != confirmPassword:
            raise serializers.ValidationError("Password and confirm password are not equal")

        else:
            return data


class UserLoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(
        max_length=100, min_length=8, style={"input_type": "password"}
    )
    token = serializers.CharField(max_length=255, read_only=True)


class UserViewSerializer(serializers.ModelSerializer):
    # age = serializers.SerializerMethodField(method_name="compute_age")
    class Meta:
        model = User
        fields = ["user_name", "email", "password"]

    # def compute_age(self, obj):
    #     today = date.today()
    #     birth_date = obj.birth_date
    #     if birth_date!=None:
    #         age = (
    #             today.year
    #             - birth_date.year
    #             - ((today.month, today.day) < (birth_date.month, birth_date.day))
    #         )
    #         return age
    #     return None


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ["verification_code","email"]
    def validate(self, obj):
        if  obj.is_expired():
            raise ValidationError("the verification code is expired")
        else:
            return obj


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return data
class PasswordResetSerializer(serializers.Serializer):
    newPassword = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    def validate(self, data):
        newPassword = data.get("newPassword")
        confirm_password = data.get("confirm_password")
        if newPassword != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data


