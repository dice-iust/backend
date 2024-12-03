from rest_framework import generics, status
from rest_framework.response import Response
from Travels.models import Travel
from .models import Expense, Settlement
from .serializers import ExpenseSerializer, SettlementSerializer


class CreateExpenseAPIView(generics.GenericAPIView):
    serializer_class = ExpenseSerializer

    def post(self, request, travel_name):
        try:
            travel_is = Travel.objects.get(name=travel_name)
        except Travel.DoesNotExist:
            return Response({"error": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, travel_is=travel_is)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebtsAPIView(generics.GenericAPIView):
    def get(self, request, travel_name):
        try:
            travel_is = Travel.objects.get(name=travel_name)
        except Travel.DoesNotExist:
            return Response({"error": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)

        expenses = Expense.objects.filter(travel_is=travel_is)
        total_expenses = sum(expense.amount for expense in expenses)

        participants = set(user for expense in expenses for user in expense.participants.all())
        share_per_user = total_expenses / len(participants)

        user_debts = {}
        for user in participants:
            user_paid = sum(
                expense.amount
                for expense in expenses
                if expense.created_by == user
            )
            user_debts[user.user_name] = user_paid - share_per_user

        return Response({"debts": user_debts}, status=status.HTTP_200_OK)


class SettleDebtAPIView(generics.GenericAPIView):
    serializer_class = SettlementSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            settlement = serializer.save()
            settlement.is_paid = True
            settlement.save()
            return Response(
                {"message": "Debt settled successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
