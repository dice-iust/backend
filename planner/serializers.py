from rest_framework import serializers
from .models import Expense, Settlement
from django.contrib.auth import get_user_model

Users = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_name"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [ "travel", "created_by", "amount", "description", "created_at","title"]
        read_only_fields = ["created_by"]

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ["id", "payer", "receiver", "travel", "amount", "is_paid", "date"]
class AllPaymentsSerializer(serializers.ModelSerializer):
    created_by=UserSerializer()
    class Meta:
        model = Expense
        fields = ["title", "created_by", "description",'amount']
