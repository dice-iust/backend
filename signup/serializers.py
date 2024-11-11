from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date
import re

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100, min_length=6, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["user_name", "email", "password"]

    def create(self, validated_data):

        user_password = validated_data.pop("password")
        if not user_password or len(user_password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters")
        if not re.search(r"[A-Za-z]", user_password):
            raise serializers.ValidationError(
                "Password must contain at least one letter"
            )
        if not re.search(r"[0-9]", user_password):
            raise serializers.ValidationError(
                "Password must contain at least one number"
            )
        user = User(**validated_data)
        user.set_password(user_password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(
        max_length=100, min_length=8, style={"input_type": "password"}
    )
    token = serializers.CharField(max_length=255, read_only=True)


class UserViewSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(method_name="compute_age")
    image_url = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ["image_url","name","last_name","user_name", "email", "password", "birth_date", "age", "city", "gender"]

    def compute_age(self, obj):
        today = date.today()
        birth_date = obj.birth_date
        if birth_date!=None:
            age = (
                today.year
                - birth_date.year
                - ((today.month, today.day) < (birth_date.month, birth_date.day))
            )
            return age
        return None
