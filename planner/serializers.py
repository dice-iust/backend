from rest_framework import serializers
from .models import Expense, Settlement

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "travel", "created_by", "amount", "description", "is_settled", "created_at"]
        read_only_fields = ["created_by"]

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ["id", "payer", "receiver", "travel", "amount", "is_paid", "date"]
