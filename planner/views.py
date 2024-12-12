import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Expense, Settlement
from .serializers import ExpenseSerializer, SettlementSerializer, AllPaymentsSerializer
from Travels.models import TravellersGroup, Travel
from django.core.files.storage import default_storage

User = get_user_model()


class CreateExpenseAPIView(APIView):
    serializer_class = ExpenseSerializer

    def post(self, request):
        # Retrieve travel name and user token from request
        travel_name = request.data.get("travel_name")
        user_token = request.headers.get("Authorization")

        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        # Retrieve user based on the token
        user = User.objects.filter(user_name=payload["user_name"]).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Retrieve travel group associated with the travel name
            travel_pay = Travel.objects.get(name=travel_name)
            travel_group = TravellersGroup.objects.get(travel_is=travel_pay)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is part of the travel group
        if user not in travel_group.users.all():
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)

        # Sync the participants
        participant_usernames = request.data.get("participants", [])
        participants = []
        for username in participant_usernames:
            participant = User.objects.filter(user_name=username).first()
            if participant:
                participants.append(participant)
            else:
                return Response({"message": f"User {username} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the receipt_image if present
        receipt_image = request.FILES.get('receipt_image')  # This handles file uploads in Postman
        if receipt_image:
            # Store the image using Django's file storage system
            file_path = default_storage.save('receipts/' + receipt_image.name, receipt_image)

        # Prepare the data for the Expense serializer
        data = request.data.copy()
        if receipt_image:
            data['receipt_image'] = file_path  # Save the image path to the database

        # Validate and save the expense
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            expense = serializer.save(created_by=user, travel=travel_group)
            expense.participants.set(participants)  # Sync participants
            expense.save()  # Save the expense object

            # Return the serialized data, including the category_icon and receipt_image URL
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

        user = User.objects.filter(user_name=payload["user_name"]).first()
        if not user:
            raise AuthenticationFailed("User not found.")

        try:
            travel_name = request.data.get("travel_name")
            travel_group = TravellersGroup.objects.get(travel_is__name=travel_name)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)

        if user not in travel_group.users.all():
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)

        expenses = Expense.objects.filter(travel=travel_group)
        total_expenses = sum(expense.amount for expense in expenses)
        participants = set(travel_group.users.all())
        my_total_pay = sum(expense.amount for expense in expenses if expense.created_by == user)

        if not participants:
            return Response({"message": "No participants found."}, status=status.HTTP_400_BAD_REQUEST)

        share_per_user = total_expenses / len(participants)
        share_per_to_me = my_total_pay / len(participants)

        user_debts = {}
        for users in participants:
            settlements = Settlement.objects.filter(travel=travel_group, receiver=user, payer=users)
            if users == user:
                continue
            if settlements.exists():
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

        # Similar logic for user_should_pay
        # Reconcile debts and prepare the response
        reconciled_debts = {}
        for key in user_debts.keys():
            if key == user:
                continue
            reconciled_debts[key] = user_debts[key]

        context = {"expenses_all": total_expenses, "travel_name": travel_name}
        return Response(
            {"context": context, "debts": user_debts, "total": reconciled_debts},
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

        user = User.objects.filter(user_name=payload["user_name"]).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            settlement = serializer.save()
            settlement.is_paid = True
            settlement.save()
            return Response(
                {"message": "The debt has been settled successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllPayView(APIView):
    def get(self, request, *args, **kwargs):
        travel_name = request.data.get("travel_name")
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.filter(user_name=payload["user_name"]).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            travel_pay = Travel.objects.get(name=travel_name)
            travel_group = TravellersGroup.objects.get(travel_is=travel_pay)
        except TravellersGroup.DoesNotExist:
            return Response({"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND)

        if user not in travel_group.users.all():
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)

        expenses = Expense.objects.filter(travel=travel_group)
        serializer = AllPaymentsSerializer(expenses, many=True)
        return Response({"pays": serializer.data}, status=status.HTTP_200_OK)
