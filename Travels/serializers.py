from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Travel
from editprofile.models import UserProfile

Users = get_user_model()


class TravelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name"]

class PhotoSerializer(serializers.ModelSerializer):
    user = TravelUserSerializer()  
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ["user", "profile_picture"]

class TravelSerializer(serializers.ModelSerializer):
    admin = PhotoSerializer()  
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