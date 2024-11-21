from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Travel,EmailAddress
# from editprofile.models import UserProfile

Users = get_user_model()

class PhotoSerializer(serializers.ModelSerializer):  
    phrofile_image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Users
        fields = ["user_name", "phrofile_image"]

    def get_image(self, obj):
        if obj.profilePicture and hasattr(obj.profilePicture, "url"):
            return self.context["request"].build_absolute_uri(obj.profilePicture.url)
        return None  

class EmailSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = EmailAddress
        fields = ("email_all",)
        
    
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
        if obj.photo and hasattr(obj.photo, "url"):
            return self.context["request"].build_absolute_uri(obj.photo.url)
        return None
