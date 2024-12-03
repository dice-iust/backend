from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Travel,EmailAddress,TravellersGroup,TravelUserRateMoney,TravelUserRateSleep
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
            "mode","rate"
        ]

    def get_image(self, obj):
        if obj.photo and hasattr(obj.photo, "url"):
            return self.context["request"].build_absolute_uri(obj.photo.url)
        return None


class TravelGetSerializer(serializers.ModelSerializer):
    admin = PhotoSerializer(context={"request": serializers.CurrentUserDefault()})
    image_url = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Travel
        fields = [
            "admin",
            "image_url",
            "name",
            "travellers",
            "start_date",
            "end_date",
            "start_place",
            "destination",
            "transportation",
            "mode",
            "description",
            "status",
            "rate",
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
    photo=serializers.ImageField()
    class Meta:
        model = Travel
        fields = [
            "photo",
            "name",
            "travellers",
            "start_date",
            "end_date",
            "start_place",
            "destination",
            "description",
            "transportation",
            "mode","status"
        ]


class UserRateSerializer(serializers.Serializer):
    user_name=serializers.CharField(max_length=255)
    rate=serializers.IntegerField()

class TravelRateSerializer(serializers.Serializer):
    travel_name = serializers.CharField(max_length=255)
    rate=serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name"]


class TravelUserRateMoneySerializer(serializers.ModelSerializer):
    travel = TravelSerializer()
    user_rated=UserSerializer()
    rated_by=UserSerializer()
    class Meta:
        model = TravelUserRateMoney
        fields = ["travel","user_rated","rated_by","rate"]


class TravelUserRateSleepSerializer(serializers.ModelSerializer):
    travel = TravelSerializer()
    user_rated = UserSerializer()
    rated_by = UserSerializer()

    class Meta:
        model = TravelUserRateSleep
        fields = ["travel", "user_rated", "rated_by", "rate"]


class UserMiddleRateSerializer(serializers.Serializer):
    travel_name = serializers.CharField(max_length=255)
    user_name = serializers.CharField(max_length=255)
    rate_sleep = serializers.IntegerField(required=False)
    rate_money = serializers.IntegerField(required=False)
