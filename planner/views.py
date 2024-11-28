from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Travels.models import Travel
from .models import Expense
from .serializers import ExpenseSerializer, SettlementSerializer


class CreateExpenseAPIView(APIView):
    def post(self, request, travel_id):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            travel = Travel.objects.get(pk=travel_id)
            serializer.save(created_by=request.user, travel=travel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebtsAPIView(APIView):
    def get(self, request, travel_id):
        travel = Travel.objects.get(pk=travel_id)
        expenses = Expense.objects.filter(travel=travel)
        total_expenses = sum(expense.amount for expense in expenses)

        participants = set(user for expense in expenses for user in expense.participants.all())
        share_per_user = total_expenses / len(participants)

        user_debts = {}
        for user in participants:
            user_paid = sum(expense.amount for expense in expenses if expense.created_by == user)
            user_debts[user.user_name] = user_paid - share_per_user

        return Response({"debts": user_debts}, status=status.HTTP_200_OK)


class SettleDebtAPIView(APIView):
    def post(self, request):
        serializer = SettlementSerializer(data=request.data)
        if serializer.is_valid():
            settlement = serializer.save()
            settlement.is_paid = True
            settlement.save()
            return Response({"message": "Debt settled successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
