from rest_framework import serializers
from .models import Expense , Settlement


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "travel", "amount", "description", "participants", "is_settled", "created_at"]


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ["id", "payer", "receiver", "travel", "amount", "is_paid"]
