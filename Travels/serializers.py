from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Travel,EmailAddress,TravellersGroup
# from editprofile.models import UserProfile

Users = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    phrofile_image = serializers.SerializerMethodField("get_image")
    class Meta:
        model = Users
        fields = ["user_name", "firstName", "phrofile_image","birthDate"]

    def get_image(self, obj):
        if obj.profilePicture and hasattr(obj.profilePicture, "url"):
            return self.context["request"].build_absolute_uri(obj.profilePicture.url)
        return None


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


class TravelGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = [
            "name",
        ]

    def get_image(self, obj):
        if obj.photo and hasattr(obj.photo, "url"):
            return self.context["request"].build_absolute_uri(obj.photo.url)
        return None


class TravelGroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    travel_is = TravelSerializer()
    class Meta:
        model = TravellersGroup
        fields = ["travel_is", "users"]


class TravelPostGroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def validate_name(self, value):
        if not Travel.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Travel with the specified name does not exist."
            )
        return value  


class TravelPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Travel
        fields = [
            "travellers",
            "name",
            "start_date",
            "end_date",
            "photo",
            "destination",
            "transportation",
            "start_place",
            "mode",
        ]


class UserRateSerializer(serializers.Serializer):
    user_name=serializers.CharField(max_length=255)
    rate=serializers.IntegerField()
    # def validate_rate(self, rate):
    #     if rate<0 or rate>5:
    #         return serializers.ValidationError("Rate is 0 to 5")
    #     return rate
