from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Travel

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_name"]


class TravelSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Travel
        fields = [
            "admin",
            "name",
            "start_date",
            "end_date",
            "photo",
            "destination",
            "transportation",
            "start_place",
            "mode",
        ]
