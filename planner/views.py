from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from Travels.models import Travel
from .models import Expense, Settlement
from .serializers import ExpenseSerializer, SettlementSerializer



class CreateExpenseAPIView(generics.GenericAPIView):
    serializer_class = ExpenseSerializer


    def post(self, request, travel_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            travel = Travel.objects.get(pk=travel_id)
            serializer.save(created_by=request.user, travel=travel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, travel_id):
        travel = Travel.objects.get(pk=travel_id)
        expenses = Expense.objects.filter(travel=travel)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DebtsAPIView(generics.GenericAPIView):


    def get(self, request, travel_id):
        travel = Travel.objects.get(pk=travel_id)
        expenses = Expense.objects.filter(travel=travel)


        total_expenses = sum(expense.amount for expense in expenses)
        participants = set(
            user for expense in expenses for user in expense.participants.all())

        if not participants:
            return Response({"message": "No participants found."}, status=status.HTTP_400_BAD_REQUEST)


        share_per_user = total_expenses / len(participants)

        user_debts = {}
        for user in participants:

            user_paid = sum(expense.amount for expense in expenses if expense.created_by == user)
            debt = user_paid - share_per_user
            user_debts[user.user_name] = debt


        results = {}
        for user, debt in user_debts.items():
            if debt < 0:
                results[user] = f"{abs(debt)} Dollars must pay"
            elif debt > 0:
                results[user] = f"{abs(debt)} The dollar has paid more than its share."
            else:
                results[user] = "There is no debt"

        return Response({"debts": results}, status=status.HTTP_200_OK)



class SettleDebtAPIView(generics.GenericAPIView):
    serializer_class = SettlementSerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            settlement = serializer.save()
            settlement.is_paid = True
            settlement.save()
            return Response({"message": "The debt has been settled successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        settlements = Settlement.objects.all()
        serializer = SettlementSerializer(settlements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)