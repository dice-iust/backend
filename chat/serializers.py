from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatMessage, TravellersGroup
Users = get_user_model()

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["sender", "message", "timestamp", "travel_name"]
