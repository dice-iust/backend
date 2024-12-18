from rest_framework import serializers
from .models import Expense, Settlement
from django.contrib.auth import get_user_model

Users = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name"]

class ExpenseSerializer(serializers.ModelSerializer):
    category_icon = serializers.SerializerMethodField()
    participants = serializers.SlugRelatedField(
        many=True, slug_field="user_name", queryset=Users.objects.all()
    )
    payer = serializers.SlugRelatedField(slug_field="user_name", queryset=Users.objects.all())
    receipt_image = serializers.ImageField(required=False)

    class Meta:
        model = Expense
        fields = [
            "amount",
            "created_at",
            "title",
            "category",
            "category_icon",
            "participants",
            "payer",
            "description",
            "receipt_image",
        ]

    def get_category_icon(self, obj):

        icon_path = obj.category_icon  
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(icon_path)
        return icon_path  

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name","profilePicture"]


class GetExpenseSerializer(serializers.ModelSerializer):
    category_icon = serializers.SerializerMethodField()
    participants = GetUserSerializer(many=True)
    payer = GetUserSerializer()
    receipt_image = serializers.ImageField(required=False)

    class Meta:
        model = Expense
        fields = [
            "amount",
            "created_at",
            "title",
            "category",
            "category_icon",
            "participants",
            "payer",
            "description",
            "receipt_image",
        ]

    def get_category_icon(self, obj):
        """Return the full URL of the category icon based on the category."""
        icon_path = obj.category_icon  # Get the relative path from the model's property
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(icon_path)
        return icon_path  # Fallback to relative path

    def get_image(self, obj):
        if obj.receipt_image and hasattr(obj.receipt_image, "url"):
            return self.context["request"].build_absolute_uri(obj.receipt_image.url)
        return None
