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
            "travel",
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
        return obj.category_icon


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ["id", "payer", "receiver", "travel", "amount", "is_paid", "date"]


class AllPaymentsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Expense
        fields = ["title", "created_by", "description", "amount"]
