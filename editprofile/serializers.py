from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileUpdateSerializer(serializers.ModelSerializer):

    profilePicture = serializers.SerializerMethodField("get_image")

    class Meta:
        model = User
        fields = [
            "firstName",
            "lastName",
            "city",
            "user_name",
            "profilePicture",
            "gender",
            "bio",
            "email",
            "phone",
            "birthDate",
            "password",
        ]
        extra_kwargs = {
            "password": {"required": False},
        }

    def get_image(self, obj):
        if obj.profilePicture and hasattr(obj.profilePicture, "url"):
            return self.context["request"].build_absolute_uri(obj.profilePicture.url)
        return None

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("The email must contain '@'.")
        return value

    def validate_password(self, value):
        if value:
            if len(value) < 6:
                raise serializers.ValidationError(
                    "Password must be at least 6 characters long."
                )
            if not re.search(r"[A-Za-z]", value):
                raise serializers.ValidationError(
                    "Password must contain at least one letter."
                )
            if not re.search(r"[0-9]", value):
                raise serializers.ValidationError(
                    "Password must contain at least one number."
                )
            if value.isdigit() or value.isalpha():
                raise serializers.ValidationError(
                    "Password cannot be all letters or all numbers."
                )
        return value

    def validate(self, data):
        password = data.get("password")
        if password:
            self.validate_password(password)
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        profile_picture = validated_data.pop("profilePicture", None)
        if profile_picture:
            instance.profilePicture = profile_picture

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class UserProfileUpdateSerializer2(serializers.ModelSerializer):
    profilePicture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "firstName",
            "lastName",
            "city",
            "user_name",
            "profilePicture",
            "gender",
            "bio",
            "email",
            "phone",
            "birthDate",
            "password",
        ]
        extra_kwargs = {
            "password": {"required": False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        profile_picture = validated_data.pop("profilePicture", None)
        if profile_picture:
            instance.profilePicture = profile_picture

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
