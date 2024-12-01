from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfilePageSerializer(serializers.ModelSerializer):
    profilePicture = serializers.SerializerMethodField("get_image")

    class Meta:
        model = User
        fields = [
            "user_name",
            "profilePicture",
            "bio",
        ]


    def get_image(self, obj):
        if obj.profilePicture and hasattr(obj.profilePicture, "url"):
            return self.context["request"].build_absolute_uri(obj.profilePicture.url)
        return None
