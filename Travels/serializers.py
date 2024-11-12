from rest_framework import serializers
from django.contrib.auth import get_user_model
from models import *
from datetime import date
import re

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        Model = User
        fields =['user_name']
class TravelSerializers(serializers.ModelSerializer):
    admin=UserSerializer()
    photo=serializers.ImageField(required=None)
    class Meta:
        Model = Travel
        feilds = [
            "admin",
            "name",
            "start_date",
            "end_date",
            "photo",
            "destination",
            "transportation",
            "start_place",
            "mode"
        ]
