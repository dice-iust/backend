from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Travel
# from editprofile.models import UserProfile

Users = get_user_model()

class PhotoSerializer(serializers.ModelSerializer):  
    phrofile_image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Users
        fields = ["user_name", "phrofile_image"]

    def get_image(self, obj):
        if obj.profile_picture and hasattr(obj.profile_picture, "url"):
            return self.context["request"].build_absolute_uri(obj.profile_picture.url)
        return None  


class TravelSerializer(serializers.ModelSerializer):
    admin = PhotoSerializer(context={"request": serializers.CurrentUserDefault()})
    image_url = serializers.SerializerMethodField("get_image")
    class Meta:
        model = Travel
        fields = [
            "admin",
            "travellers",
            "name",
            "start_date",
            "end_date",
            "image_url",
            "destination",
            "transportation",
            "start_place",
            "mode",
        ]

    def get_image(self, obj):
        return self.context["request"].build_absolute_uri(obj.photo.url)
