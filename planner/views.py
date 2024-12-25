import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Expense, Settlement
from .serializers import (
    ExpenseSerializer,
    GetExpenseSerializer,
    MarkAsPaidSerializer,
    PastPaymentSerializer,
)
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

        expenses = Expense.objects.filter(travel=travel_group)
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

        user_debts_to_others = {
            key: value for key, value in debts[user.user_name].items() if value < 0
        }
        others_debt_to_user = {
            key: value for key, value in debts[user.user_name].items() if value > 0
        }

        has_debt = bool(user_debts_to_others)
        has_credit = bool(others_debt_to_user)

        response_data = {
            "user_debts_to_others": user_debts_to_others,
            "others_debt_to_user": others_debt_to_user,
            "has_debt": has_debt,
            "has_credit": has_credit,
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
    def post(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed("No token provided.")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user = User.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            raise AuthenticationFailed("User not found.")

        expense = (
            Expense.objects.filter(participants=user, is_paid=False)
            .order_by("-created_at")
            .first()
        )

        if not expense:
            return Response(
                {"error": "No unpaid expenses found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        expense.is_paid = True
        expense.save()

        return Response(
            {"message": "Expense marked as paid successfully."},
            status=status.HTTP_200_OK,
        )


class MarkAsPaidAPIView(APIView):
    def post(self, request):
        # دریافت توکن از هدر درخواست
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No token provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        # دیکد کردن توکن و دریافت اطلاعات کاربر
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.InvalidTokenError:
            return Response(
                {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )

        # پیدا کردن کاربر با استفاده از user_id در توکن
        user = User.objects.filter(id=payload["user_id"]).first()
        if not user:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # سریالایزر برای گرفتن داده‌های درخواست
        serializer = MarkAsPaidSerializer(data=request.data)
        if serializer.is_valid():
            expense_id = serializer.validated_data.get("expense_id")
            receiver_username = serializer.validated_data.get("receiver_username")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # پیدا کردن دریافت‌کننده با یوزرنیم
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response(
                {"error": "Receiver user not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # پیدا کردن هزینه‌ای که باید به‌عنوان پرداخت‌شده علامت‌گذاری شود
        try:
            expense = Expense.objects.get(id=expense_id, is_paid=False)
        except Expense.DoesNotExist:
            return Response(
                {"error": "Expense not found or already paid."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # محاسبه سهم پرداخت هر نفر
        split_amount = expense.calculate_split()

        # بررسی اینکه آیا کاربر جزو شرکت‌کنندگان در هزینه است
        if user not in expense.participants.all():
            return Response(
                {"error": "User is not a participant in this expense."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # بررسی اینکه آیا دریافت‌کننده جزو شرکت‌کنندگان در هزینه است
        if receiver not in expense.participants.all():
            return Response(
                {"error": "Receiver is not a participant in this expense."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # علامت‌گذاری هزینه به‌عنوان پرداخت‌شده
        expense.is_paid = True
        expense.save()

        # ثبت تاریخچه پرداخت‌ها و تسویه‌حساب‌ها
        with transaction.atomic():
            # تسویه‌حساب بین کاربر و دریافت‌کننده
            Settlement.objects.create(
                payer=user,
                receiver=receiver,
                amount=split_amount,
                travel=expense.travel,
                is_paid=True,
            )

            # ثبت پرداخت‌های گذشته برای هر دو طرف (کاربر و دریافت‌کننده)
            PastPayment.objects.create(
                user=user,
                expense=expense,
                amount=split_amount,
                description=f"Payment for {expense.title} marked as paid",
            )
            PastPayment.objects.create(
                user=receiver,
                expense=expense,
                amount=split_amount,
                description=f"Payment received for {expense.title}",
            )

        return Response(
            {"message": "Expense marked as paid and past payments recorded."},
            status=status.HTTP_200_OK,
        )
