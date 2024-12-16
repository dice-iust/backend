import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Expense, Settlement
from .serializers import ExpenseSerializer, GetExpenseSerializer
from Travels.models import TravellersGroup, Travel
from django.core.files.storage import default_storage

User = get_user_model()


class CreateExpenseAPIView(APIView):
    serializer_class = ExpenseSerializer

    def get(self, request):
        context = {
            "accommodation": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/accommodation.jpg",
            "Entertainment": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Entertainment.jpg",
            "Groceries": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Groceries.jpg",
            "Healthcare": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Healthcare.jpg",
            "Insurance": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Insurance.jpg",
            "Other": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Other.jpg",
            "Rent": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Rent.jpg",
            "Restaurant": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Restaurant.jpg",
            "Shopping": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Shopping.jpg",
            "Transport": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Transport.jpg",
        }

        travel_name = request.query_params.get("travel_name")
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
            return Response(
                {"detail": "User not found.", "context": context},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            travel_pay = Travel.objects.filter(name=travel_name).first()
            travel_group = TravellersGroup.objects.get(travel_is=travel_pay)
        except TravellersGroup.DoesNotExist:
            return Response(
                {"message": "Travel not found.", "context": context},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user not in travel_group.users.all() and user != travel_pay.admin:
            return Response(
                {
                    "message": "You are not a participant in this travel.",
                    "context": context,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        participants_in_travel = travel_group.users.all()
        if travel_pay.admin not in participants_in_travel:
            participants_in_travel = participants_in_travel | User.objects.filter(
                user_id=travel_pay.admin.user_id
            )

        valid_participants = [
            {"user_name": participant.user_name}
            for participant in participants_in_travel
        ]

        return Response(
            {"context": context, "valid_participants": valid_participants},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        context = {
            "accommodation":f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/accommodation.jpg",
            "Entertainment": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Entertainment.jpg",
            "Groceries": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Groceries.jpg",
            "Healthcare": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Healthcare.jpg",
            "Insurance": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Insurance.jpg",
            "Other": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Other.jpg",
            "Rent": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Rent.jpg",
            "Restaurant": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Restaurant.jpg",
            "Shopping": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Shopping.jpg",
            "Transport": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}icons/Transport.jpg",
        }
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

        user = User.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found.","context":context}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            travel_pay = Travel.objects.filter(name=travel_name).first()
            travel_group = TravellersGroup.objects.get(travel_is=travel_pay)
        except TravellersGroup.DoesNotExist:
            return Response(
                {"message": "Travel not found.","context":context}, status=status.HTTP_404_NOT_FOUND
            )

        if user not in travel_group.users.all() and user!=travel_pay.admin:
            return Response(
                {"message": "You are not a participant in this travel.","context":context},
                status=status.HTTP_403_FORBIDDEN,
            )
        participants_in_travel = travel_group.users.all() 
        if travel_pay.admin not in participants_in_travel:
            participants_in_travel = participants_in_travel | {travel_pay.admin} 
        participant_usernames = request.data.get("participants", [])
        participants = []
        for username in set(participant_usernames):
            participant = User.objects.filter(user_name=username).first()
            if participant:
                participants.append(participant)
            else:
                return Response(
                    {"message": f"User {username} does not exist.","context":context},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )  
        if serializer.is_valid():
            if request.data.get("receipt_image"):
                expense = serializer.save(travel=travel_group)
                expense.participants.set(participants)
                expense.save(receipt_image=request.data.get("receipt_image"))
                return Response(
                    {
                        "data": serializer.data,
                        "context": context,
                        "valid_participants": [
                            {"user_name": participant.user_name}
                            for participant in participants_in_travel
                        ],
                    },
                    status=status.HTTP_201_CREATED,
                )

            expense = serializer.save(travel=travel_group)
            expense.participants.set(participants)
            expense.save()
            return Response({"data":serializer.data,
                            "context": context,"valid_participants": [{"user_name": participant.user_name} for participant in participants_in_travel],} ,status=status.HTTP_201_CREATED)

        return Response({"error":serializer.errors,"context":context}, status=status.HTTP_400_BAD_REQUEST)


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
            travel_name = request.query_params.get("travel_name")
            travel = Travel.objects.filter(name=travel_name).first()
            travel_group = TravellersGroup.objects.get(travel_is__name=travel_name)
        except TravellersGroup.DoesNotExist:
            return Response(
                {"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if user not in travel_group.users.all() and user != travel.admin:
            return Response(
                {"message": "You are not a participant in this travel."},
                status=status.HTTP_403_FORBIDDEN,
            )

        debts = {
            participant.user_name: {
                participant.user_name: 0 for participant in travel_group.users.all()
            }
            for participant in travel_group.users.all()
        }

        expenses = Expense.objects.filter(travel=travel_group)

        for expense in expenses:
            participants = expense.participants.all()
            total_participants = len(participants) + 1 
            share_per_user = (
                expense.amount / total_participants if total_participants else 0
            )

            for participant in participants:
                if participant == user or expense.payer == user:
                    if expense.payer == user and participant != user:
                        debts[participant.user_name][user.user_name] += share_per_user
                        debts[user.user_name][participant.user_name] -= share_per_user
                    elif expense.payer != user:

                        debts[user.user_name][expense.payer.user_name] += share_per_user
                        debts[expense.payer.user_name][user.user_name] -= share_per_user

        user_debts = debts.get(user.user_name, {})

        user_debts = {key: value for key, value in user_debts.items() if value != 0}

        has_debt = bool(user_debts)

        response_data = {
            "user_debt_info": {user.user_name: user_debts},
            "has_debt": has_debt,
            "photo": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}/payment.jpg",
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AllPayView(APIView):
    def get(self, request, *args, **kwargs):
        travel_name = request.query_params.get("travel_name")
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

        if user not in travel_group.users.all() and user!=travel_pay.admin:
            return Response({"message": "You are not a participant in this travel."}, status=status.HTTP_403_FORBIDDEN)

        expenses = Expense.objects.filter(travel=travel_group)
        serializer = GetExpenseSerializer(
            expenses, many=True, context={"request": request}
        )
        return Response({"pays": serializer.data}, status=status.HTTP_200_OK)
