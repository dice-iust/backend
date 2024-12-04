import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Expense,Settlement
from .serializers import ExpenseSerializer,SettlementSerializer
from Travels.models import TravellersGroup, Travel

User = get_user_model()

class CreateExpenseAPIView(APIView):
    serializer_class = ExpenseSerializer

    def post(self, request, travel_name):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")
        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            travel_pay = Travel.objects.get(name=travel_name)
            travel_group = TravellersGroup.objects.get(travel_is=travel_pay)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travellers Group not found."}, status=status.HTTP_404_NOT_FOUND)

        if user not in travel_group.users.all():
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user, travel=travel_group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebtsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            raise AuthenticationFailed("User not found.")
        try:
            travel_name=request.data.get('travel_name')
            travel_group = TravellersGroup.objects.get(travel_is__name=travel_name)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)

        if user not in travel_group.users.all():
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)
        travel_name=request.data.get('travel_name')
        expenses = Expense.objects.filter(travel=travel_group)
        total_expenses = sum(expense.amount for expense in expenses)
        participants = set(travel_group.users.all())
        my_total_pay = sum(expense.amount for expense in expenses if expense.created_by==user)
        if not participants:
            return Response({"message": "No participants found."}, status=status.HTTP_400_BAD_REQUEST)

        share_per_user = total_expenses / len(participants)
        share_per_to_me = my_total_pay/len(participants)

        user_debts = {}
        for users in participants:
            settlements = Settlement.objects.filter(
                travel=travel_group, receiver=user, payer=users
            )
            if users == user:
                #     user_debts[users.user_name] = {
                #         "total_share": share_per_to_me,
                #         "amount_paid": share_per_to_me,
                #         "remaining_debt": 0,
                #     }
                continue
            if settlements.exists():  # Ensure there are settlements before processing
                total_paid_by_participant = sum(settlement.amount for settlement in settlements)
                user_paid = total_paid_by_participant
                debt = share_per_to_me - total_paid_by_participant
                user_debts[users.user_name] = {
                    "total_share": share_per_to_me,
                    "amount_paid": user_paid,
                    "remaining_debt": debt,
                }
            else:
                user_debts[users.user_name] = {
                    "total_share": share_per_to_me,
                    "amount_paid": 0,
                    "remaining_debt": share_per_to_me,
                }

        user_should_pay={}
        for part in participants:
            if part == user:
                #     user_should_pay[part.user_name] = {
                #         "total_share": others_expenses,
                #         "amount_paid": others_expenses,
                #         "remaining_debt": 0,
                #     }
                continue
            others_expenses = my_total_pay = sum(
            expense.amount for expense in expenses if expense.created_by == part
                )/len(participants)
            if not others_expenses:
                continue
            settlements = Settlement.objects.filter(
                travel=travel_group, receiver=part, payer=user
            )
            if settlements.exists():  # Ensure there are settlements before processing
                total_paid_by_participant = sum(settlement.amount for settlement in settlements)
                user_paid = total_paid_by_participant
                debt = others_expenses - total_paid_by_participant
                user_should_pay[part.user_name] = {
                    "total_share": others_expenses,
                    "amount_paid": total_paid_by_participant,
                    "remaining_debt": debt,
                }
            user_should_pay[part.user_name] = {
                "total_share": others_expenses,
                "amount_paid": 0,
                "remaining_debt": others_expenses,
            }
        reconciled_debts = {}

        for key in user_debts.keys():
            if key==user:
                continue
            if key not in user_should_pay:
                reconciled_debts[key] = user_debts[key]
            else:
                user_debt = user_debts[key]["remaining_debt"]
                amount_to_pay = user_should_pay[key]["remaining_debt"]
                reconciled_debts[key] = {
                    "total_share": user_debts[key]["total_share"],
                    "amount_paid": user_debts[key]["amount_paid"],
                    "remaining_debt": user_debt,
                }
                if amount_to_pay >= user_debt:
                    reconciled_debts[key]["remaining_debt"] = 0
                    user_should_pay[key]["amount_paid"] -= user_debt
                else:
                    reconciled_debts[key]["remaining_debt"] -= amount_to_pay
                    reconciled_debts[key]["amount_paid"] += amount_to_pay
                    user_should_pay[key]["remaining_debt"] = 0
                    user_should_pay[key]["amount_paid"] = amount_to_pay
        context={
            "expenses_all": total_expenses,
            "travel_name":travel_name
        }
        return Response(
            {
                "context":context,
                "debts": user_debts,
                "my_debts": user_should_pay,
                "total": reconciled_debts,
            },
            status=status.HTTP_200_OK,
        )


class SettleDebtAPIView(APIView):
    serializer_class = SettlementSerializer

    def post(self, request):

        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            settlement = serializer.save()
            settlement.is_paid = True
            settlement.save()
            return Response({"message": "The debt has been settled successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
