import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Expense, Settlement, PastPayment, ExpensePayment
from .serializers import (
    ExpenseSerializer,
    GetExpenseSerializer,
    MarkAsPaidSerializer,
    PastPaymentSerializer,
    MarkDebtAsPaidSerializer,
    GetPastPaySerializer,
    GetUserSerializer,
)
from Travels.models import TravellersGroup, Travel
from django.core.files.storage import default_storage
from django.db.models import F, ExpressionWrapper, DurationField, Q
User = get_user_model()
from signup.models import BlacklistedToken
from Travels.serializers import PhotoSerializer, TravelGroupSerializer
from django.db.models import Count, F, ExpressionWrapper, FloatField

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
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
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
                {"detail": "User not found.", "context": context},
                status=status.HTTP_404_NOT_FOUND,
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        try:
            travel_pay = Travel.objects.filter(name=travel_name).first()
            if not travel_pay:
                return Response(
                    {"message": "Travel not found.", "context": context},
                    status=status.HTTP_404_NOT_FOUND,
                )

            travel_group = TravellersGroup.objects.filter(travel_is=travel_pay).first()
            if not travel_group:
                return Response(
                    {"message": "Travel group not found.", "context": context},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {
                    "message": f"Error fetching travel group: {str(e)}",
                    "context": context,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

        participants_data = request.data.get("participants", "")
        if isinstance(participants_data, str):
            participants_usernames = [
                username.strip()
                for username in participants_data.split(",")
                if username.strip()
            ]
        elif isinstance(participants_data, list):
            participants_usernames = participants_data
        else:
            return Response(
                {"message": "Invalid participants format.", "context": context},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants_data = request.data.get("participants", "")
        if isinstance(participants_data, str):
            participants_usernames = [
                username.strip()
                for username in participants_data.split(",")
                if username.strip()
            ]
        elif isinstance(participants_data, list):
            participants_usernames = participants_data
        else:
            return Response(
                {"message": "Invalid participants format.", "context": context},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = []
        for participant_username in participants_usernames:
            participant = User.objects.filter(user_name=participant_username).first()
            if participant:
                participants.append(participant)
            else:
                return Response(
                    {
                        "message": f"User {participant_username} does not exist.",
                        "context": context,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            expense = serializer.save(travel=travel_group)
            expense.participants.set(participants)
            e=ExpensePayment.objects.create(travel=travel_group,
            amount=expense.amount,payer=expense.payer)
            e.participants.set(participants)
            e.save()
            if "receipt_image" in request.data:
                expense.receipt_image = request.data.get("receipt_image")
                expense.save()

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

        return Response(
            {"error": serializer.errors, "context": context},
            status=status.HTTP_400_BAD_REQUEST,
        )


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
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response(
                "Token has been invalidated.", status=status.HTTP_403_FORBIDDEN
            )
        try:
            travel_name = request.query_params.get("travel_name")
            travel = Travel.objects.filter(name=travel_name).first()
            travel_group = TravellersGroup.objects.get(travel_is__name=travel_name)
        except (Travel.DoesNotExist, TravellersGroup.DoesNotExist):
            return Response(
                {"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if user not in travel_group.users.all() and user != travel.admin:
            return Response(
                {"message": "You are not a participant in this travel."},
                status=status.HTTP_403_FORBIDDEN,
            )

        participants_in_travel = list(travel_group.users.all())
        if travel.admin not in participants_in_travel:
            participants_in_travel.append(travel.admin)

        debts = {
            participant.user_name: {
                other.user_name: 0.0 for other in participants_in_travel
            }
            for participant in participants_in_travel
        }

        expenses = ExpensePayment.objects.filter(travel=travel_group)
        for expense in expenses:
            participants = list(expense.participants.all())
            total_participants = len(participants)
            share_per_user = (
                float(expense.amount) / total_participants if total_participants else 0
            )

            for participant in participants:
                if participant != expense.payer:
                    debts[expense.payer.user_name][
                        participant.user_name
                    ] += share_per_user
                    debts[participant.user_name][
                        expense.payer.user_name
                    ] -= share_per_user

        user_debts_to_others = [
            {
                "user": GetUserSerializer(
                    User.objects.filter(user_name=key).first(),
                    context={"request": self.request},
                ).data,
                "amount": value,
            }
            for key, value in debts[user.user_name].items()
            if value < 0
        ]

        others_debt_to_user = [
            {
                "user": GetUserSerializer(
                    User.objects.filter(user_name=key).first(),
                    context={"request": self.request},
                ).data,
                "amount": value,
            }
            for key, value in debts[user.user_name].items()
            if value > 0
        ]

        has_debt = bool(user_debts_to_others)
        has_credit = bool(others_debt_to_user)
        pays = PastPayment.objects.filter(
            Q(travel=travel_group, payer=user) | Q(travel=travel_group, receiver=user)
        )
        if not pays:
            response_data = {
                "user_debts_to_others": user_debts_to_others,
                "others_debt_to_user": others_debt_to_user,
                "has_debt": has_debt,
                "has_credit": has_credit,
                "photo": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}payment.jpg",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        past_serializer = GetPastPaySerializer(
            pays, many=True, context={"request": self.request}
        ).data
        response_data = {
            "user_debts_to_others": user_debts_to_others,
            "others_debt_to_user": others_debt_to_user,
            "has_debt": has_debt,
            "has_credit": has_credit,
            "past_serializer": past_serializer,
            "photo": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}payment.jpg",
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
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        try:
            travel_pay = Travel.objects.filter(name=travel_name).first()
            travel_group = TravellersGroup.objects.filter(travel_is=travel_pay).first()
        except TravellersGroup.DoesNotExist:
            return Response(
                {"message": "Travel not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if user not in travel_group.users.all() and user != travel_pay.admin:
            return Response(
                {"message": "You are not a participant in this travel."},
                status=status.HTTP_403_FORBIDDEN,
            )

        expenses = Expense.objects.filter(travel=travel_group)
        serializer = GetExpenseSerializer(
            expenses, many=True, context={"request": request}
        )
        return Response({"pays": serializer.data}, status=status.HTTP_200_OK)


class MarkAsPaidAPIView(APIView):   
    def get(self, request):
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
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        travel_name=request.query_params.get('travel_name')
        travel_choose=Travel.objects.filter(name=travel_name).first()
        if not travel_choose:
            return Response("travel not found", status=status.HTTP_404_NOT_FOUND)
        tg=TravellersGroup.objects.filter(travel_is=travel_choose).first()
        if not tg:
            return Response("travel not found", status=status.HTTP_404_NOT_FOUND)
        pays=PastPayment.objects.filter(Q(travel=tg,payer=user) | Q(travel=tg,receiver=user))
        if not pays:
            return Response("payment not found", status=status.HTTP_404_NOT_FOUND)
        serializer = GetPastPaySerializer(
            pays, many=True, context={"request": self.request}
        ).data
        return Response(
            serializer,
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
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
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.", status=status.HTTP_403_FORBIDDEN)

        serializer = MarkDebtAsPaidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        payee_username = serializer.validated_data.get("payee")
        payer_user = User.objects.filter(user_name=payee_username).first()
        amount = serializer.validated_data.get("amount")
        travel_name = serializer.validated_data.get("travel_name")
        travel = Travel.objects.filter(name=travel_name).first()
        if not travel:
            return Response("Travel not found", status=status.HTTP_404_NOT_FOUND)

        tg = TravellersGroup.objects.filter(travel_is=travel).first()
        if not tg:
            return Response("Travel not found", status=status.HTTP_404_NOT_FOUND)

        expens = ExpensePayment.objects.filter(
            travel=tg, payer=payer_user, participants=user
        ).first()
        if not expens:
            return Response("Expense not found", status=status.HTTP_404_NOT_FOUND)

        expens1 = Expense.objects.filter(
            travel=tg, payer=payer_user, participants=user
        ).first()
        if not expens1:
            return Response("Expense not found", status=status.HTTP_404_NOT_FOUND)

        if not payer_user:
            return Response(
                {"message": f"User {payee_username} does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = list(expens.participants.all())
        if not participants:
            return Response("No users found", status=status.HTTP_400_BAD_REQUEST)

        past_payment = PastPayment.objects.create(
            payer=user, receiver=payer_user, amount=amount, travel=tg, Expenses=expens1
        )
        if not past_payment:
            return Response("Payment not found", status=status.HTTP_404_NOT_FOUND)

        other_expenses = (
            ExpensePayment.objects.filter(travel=tg, payer=payer_user, participants=user)
            .annotate(
                participant_count=Count("participants"),
                amount_per_participant=ExpressionWrapper(
                    F("amount") / F("participant_count"), output_field=FloatField()
                ),
            )
            .order_by("-amount_per_participant")
        )

        for other_expense in other_expenses:
            if amount <= 0:
                break

            participants = list(other_expense.participants.all())
            if not participants:
                continue

            expens_amont = other_expense.amount / len(participants)
            if amount >= expens_amont:
                other_expense.participants.remove(user)
                other_expense.amount -= expens_amont
                amount -= expens_amont
            else:
                other_expense.participants.remove(user)
                other_expense.amount -= amount
                amount = 0
            other_expense.save()

        if amount > 0:
            return Response(
                "Remaining amount could not be cleared due to insufficient expenses.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": f"Payment of ${serializer.validated_data.get('amount')} from {user.user_name} to {payee_username} has been recorded."
            },
            status=status.HTTP_200_OK,
        )
