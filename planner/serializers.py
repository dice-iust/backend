from rest_framework import serializers
from Travels.serializers import TravelSerializer, UserSerializer
from .models import Expense, Settlement

class ExpenseSerializer(serializers.ModelSerializer):
    travel_is = TravelSerializer()
    participants = UserSerializer(many=True)
    created_by = UserSerializer()

    class Meta:
        model = Expense
        fields = [
            "id",
            "travel_is",
            "created_by",
            "amount",
            "description",
            "participants",
            "is_settled",
            "created_at",
        ]


class SettlementSerializer(serializers.ModelSerializer):
    travel_is = TravelSerializer()
    payer = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Settlement
        fields = [
            "id",
            "payer",
            "receiver",
            "travel_is",
            "amount",
            "is_paid",
            "date",
        ]
