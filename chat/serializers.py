from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatMessage
Users = get_user_model()
from Travels.models import Travel, TravellersGroup
Users = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name"]

class ChatSerializer(serializers.ModelSerializer):
    sender=UserSerializer()
    class Meta:
        model = ChatMessage
        fields = ["sender", "message", "timestamp", "travel_name"]
class GetProfileSerializer(serializers.ModelSerializer):
    profilePicture = serializers.SerializerMethodField("get_image")
    class Meta:
        model =Users
        fields = ["user_name","firstName","lastName","profilePicture","bio","birthDate"]
    def get_image(self, obj):
        if obj.profilePicture and hasattr(obj.profilePicture, "url"):
            return self.context["request"].build_absolute_uri(obj.profilePicture.url)
        return None
