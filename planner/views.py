import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Expense
from .serializers import ExpenseSerializer
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

        uuser = User.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


        try:
            travel_pay=Travel.objects.filter(name=travel_name)
            travel_group = TravellersGroup.objects.get(travel_is=travel_pay)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)

        if user not in travel_group.users.all():
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user, travel=travel_group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebtsAPIView(APIView):
    def get(self, request, travel_name, *args, **kwargs):
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
            travel_group = TravellersGroup.objects.get(travel_is__name=travel_name)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)


        if user not in travel_group.users.all():
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)


        expenses = Expense.objects.filter(travel=travel_group)
        total_expenses = sum(expense.amount for expense in expenses)
        participants = set(travel_group.users.all())

        if not participants:
            return Response({"message": "No participants found."}, status=status.HTTP_400_BAD_REQUEST)

        share_per_user = total_expenses / len(participants)

        user_debts = {}
        for user in participants:
            user_paid = sum(expense.amount for expense in expenses if expense.created_by == user)
            debt = user_paid - share_per_user
            user_debts[user.user_name] = {
                "total_share": share_per_user,
                "amount_paid": user_paid,
                "remaining_debt": share_per_user - user_paid,
            }

        return Response({"debts": user_debts}, status=status.HTTP_200_OK)


import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SettlementSerializer
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

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
