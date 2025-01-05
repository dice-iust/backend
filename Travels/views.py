from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import (
    Travel,
    EmailAddress,
    TravellersGroup,
    UserRate,
    TravelUserRateMoney,
    TravelUserRateSleep,
    Requests,
)
from .serializers import (
    TravelSerializer,
    EmailSerializer,
    TravelGroupSerializer,
    TravelPostGroupSerializer,
    TravelPostSerializer,
    UserRateSerializer,
    TravelRateSerializer,
    TravelUserRateMoneySerializer,
    TravelUserRateSleepSerializer,
    UserMiddleRateSerializer,
    RequestSerializer,MyRatedOtherMoneySerializer,MyRatedOtherSleepSerializer
)
from datetime import datetime, timedelta
from django.db.models import F, ExpressionWrapper, DurationField, Q
from calendar import monthrange
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import generics
from django_filters import rest_framework as filters
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()
import jwt
from django.utils.timezone import now
from django.db.models import Sum
from django.core.mail import send_mail
import random
from signup.models import BlacklistedToken

class AllTravels(generics.ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    # search_fields = [
    #     # "travellers",
    #     # "admin__user_name",
    #     # "mode",
    #     # "destination",
    #     # "transportation",
    #     # "start_place",
    #     "start_date","end_date"
    # ]
    filterset_fields = ("start_date", "end_date", "start_place", "transportation",'name')


class TravelViewSpring(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        spring_travel = queryset.filter(start_date__month__in=[4, 5, 6])
        spring_serializer = TravelSerializer(
            spring_travel, many=True, context={"request": self.request}
        )
        context = {
            "Spring_Trips": spring_serializer.data,
            "photo_spring": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/SpringTrips.avif",
        }
        return Response(context, status=status.HTTP_200_OK)


class TravelViewWinter(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        winter_travel = queryset.filter(start_date__month__in=[1, 2, 3])
        winter_serializer = TravelSerializer(
            winter_travel, many=True, context={"request": self.request}
        )
        context = {
            "Winter_Trips": winter_serializer.data,
            "photo_winter": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/WinterTrips.avif",
        }
        return Response(context, status=status.HTTP_200_OK)

  
class TravelViewAutumn(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        autumn_travel = queryset.filter(start_date__month__in=[10, 11, 12])
        autumn_serializer = TravelSerializer(
            autumn_travel, many=True,context={"request": self.request}
        )
        context = {
            "Autumn_Trips": autumn_serializer.data,
            "photo_autumn": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/AutumnTrips.avif",
        }
        return Response(context, status=status.HTTP_200_OK)

 
class TravelViewSummer(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        summer_travel = queryset.filter(start_date__month__in=[7, 8, 9])
        summer_serializer = TravelSerializer(
            summer_travel, many=True, context={"request": self.request}
        )
        context = {
            "Summer_Trips": summer_serializer.data,
            "photo_summer": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/SummerTrips.avif",
        }
        return Response(context, status=status.HTTP_200_OK)


class TravelViewFancy(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        fancy_travel = queryset.filter(mode="Fancy")
        fancy_serializer = TravelSerializer(
            fancy_travel, many=True, context={"request": self.request}
        )
        context = {
            "Fancy_Trips": fancy_serializer.data,
            "photo_fancy": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/FancyTrips.avif",
        }
        return Response(context, status=status.HTTP_200_OK)


class TravelVieweconomy(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        fancy_travel = queryset.filter(mode="Budget-friendly")
        economy_serializer = TravelSerializer(
            fancy_travel, many=True, context={"request": self.request}
        )
        context = {
            "economical_Trips": economy_serializer.data,
            "photo_economy": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/economicalTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)


class TravelViewPopular(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny,]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        popular_travel = queryset.order_by("-travellers")[:15]
        travel_serializer = TravelSerializer(
            popular_travel, many=True, context={"request": self.request}
        )
        array_card = [
            {
                "id": "UpComing",
                "name": "Up comingTrips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/Upcomingtrips.avif",
            },
            {
                "id": "Short",
                "name": "Short Trips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/ShortTrips.avif",
            },
            {
                "id": "Spring",
                "name": "Spring Trips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/SpringTrips.avif",
            },
            {
                "id": "Summer",
                "name": "Summer Trips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/SummerTrips.avif",
            },
            {
                "id": "Autumn",
                "name": "Autumn Trips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/AutumnTrips.avif",
            },
            {
                "id": "Winter",
                "name": "Winter Trips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/WinterTrips.avif",
            },
            {
                "id": "Fancy",
                "name": "Fancy Trips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/FancyTrips.avif",
            },
            {
                "id": "Economical",
                "name": "economical Trips",
                "image": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}profiles/economicalTrips.avif",
            },
        ]
        context = {"Popular_Trips": travel_serializer.data, "cards": array_card}
        return Response(context, status=status.HTTP_200_OK)


class EmailView(APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email_serializer = EmailSerializer(data=request.data)

        if email_serializer.is_valid():
            email_serializer.save()
            send_mail(
            subject="Request to join travel",
            message=f"hello{email}",
            from_email="triiptide@gmail.com",
            recipient_list=[email_serializer['email']],
        )
            return Response(data=email_serializer.data, status=status.HTTP_201_CREATED)

        return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TravelViewUpcoming(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = datetime.now()
        last_day_of_month = datetime(
            today.year, today.month, monthrange(today.year, today.month)[1]
        )
        queryset = Travel.objects.all()
        upcoming_travel = queryset.filter(
            start_date__gte=today, start_date__lte=last_day_of_month
        )
        upcoming_serializer = TravelSerializer(
            upcoming_travel, many=True, context={"request": self.request}
        )
        context = {
            "Up_comingTrips": upcoming_serializer.data,
            "photo_upcoming": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/UpcomingTrips.avif",
        }
        return Response(context, status=status.HTTP_200_OK)


class TravelViewShort(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        queryset = Travel.objects.all()

        quick_travel = queryset.annotate(
            duration=ExpressionWrapper(
                F("end_date") - F("start_date"), output_field=DurationField()
            )
        ).filter(Q(duration=timedelta(days=2)) | Q(duration=timedelta(days=1)))
        short_serializer = TravelSerializer(
            quick_travel, many=True, context={"request": self.request}
        )
        context = {
            "Short_Trips": short_serializer.data,
            "photo_short": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/ShortTrips.avif",
        }
        return Response(context, status=status.HTTP_200_OK)

class SingleTravelView(APIView):
    serializer_class = TravelGroupSerializer
    permission_classes = [AllowAny]

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

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        try:
            travel_name=request.query_params.get('travel_name')
            travel_get = Travel.objects.get(name=travel_name)
        except Travel.DoesNotExist:
            return Response(
                {"detail": "This travel does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        tg=TravellersGroup.objects.filter(travel_is=travel_get).first()
        if not tg:
            return Response("this Travel is not exit.")
        travel_serializer = TravelGroupSerializer(
            tg, context={"request": request}
        )
        profile_url = request.build_absolute_uri(user.profilePicture.url) if user.profilePicture else None
        if (user == travel_get.admin):
            return Response({"travels":travel_serializer.data,"code":travel_get.key,
                "is_part":True,
                "profile":profile_url,"name":user.user_name}, status=status.HTTP_200_OK)
        if user in tg.users.all():
            return Response({"travels":travel_serializer.data,
                "profile":profile_url,"name":user.user_name,
                "is_part":True}, status=status.HTTP_200_OK)
        else:
            if travel_get.status=='Private':
                return Response({"error":"Your Not Part of Travel","is_part":False,
                "profile":profile_url,"name":user.user_name},status=status.HTTP_403_FORBIDDEN)
            return Response(
                {"travels": travel_serializer.data, "is_part": False,
                "profile":profile_url,"name":user.user_name},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "error", "is_part": False}, status=status.HTTP_404_NOT_FOUND
        )


class TravelGroupView(APIView):
    serializer_class = TravelGroupSerializer

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

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        serializer_past = None
        serializer_current = None
        serializer_future = None
        past_trips = TravellersGroup.objects.filter(
            Q(users=user) | Q(travel_is__admin=user), travel_is__end_date__lt=now()
        ).distinct()

        current_trips = TravellersGroup.objects.filter(
            Q(users=user) | Q(travel_is__admin=user),
            travel_is__start_date__lte=now(),
            travel_is__end_date__gte=now(),
        ).distinct()
        future_trips = TravellersGroup.objects.filter(
            Q(users=user) | Q(travel_is__admin=user), travel_is__start_date__gt=now()
        ).distinct()
        if past_trips.exists():
            serializer_past = TravelGroupSerializer(
                past_trips, many=True, context={"request": self.request}
            )
        if current_trips.exists():
            serializer_current = TravelGroupSerializer(
                current_trips, many=True, context={"request": self.request}
            )
        if future_trips.exists():
            serializer_future = TravelGroupSerializer(
                future_trips, many=True, context={"request": self.request}
            )
        return Response(
            {
                "past": serializer_past.data if serializer_past else [],
                "current": serializer_current.data if serializer_current else [],
                "future": serializer_future.data if serializer_future else [],
                "photo":f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels4.jpg"
            },
            status=status.HTTP_200_OK,
        )

        return Response(
            {"detail": "No travel groups found for the user."},
            status=status.HTTP_404_NOT_FOUND,
        )


class PostTravelView(APIView):
    serializer_class = TravelPostSerializer
    authenticated_classes = [TokenAuthentication]
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

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()

        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        serializer=TravelPostSerializer(data=request.data)
        if serializer.is_valid():
            if not request.data.get('photo'):
                key=random.randint(1000, 9999)
                travel =  serializer.save(admin=user,key=key)
                TravellersGroup.objects.create(travel_is=travel)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            key = random.randint(1000, 9999)
            travel =  serializer.save(admin=user,photo=request.data.get('photo'),key=key)
            TravellersGroup.objects.create(travel_is=travel)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class TravelUserRateView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Authorization token not provided.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()

        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        money_rates = TravelUserRateMoney.objects.filter(user_rated=user)
        sleep_rates = TravelUserRateSleep.objects.filter(user_rated=user)

        rates_summary = {}
        for money_rate in money_rates:
            travel = money_rate.travel
            travel_is = TravelSerializer(travel, context={"request": self.request}).data
            if travel.name not in rates_summary:
                rates_summary[travel.name] = {"travel_is": travel_is, "money_rate": None, "sleep_rate": None}

            rates_summary[travel.name]["money_rate"] = money_rate.rate

        for sleep_rate in sleep_rates:
            travel = sleep_rate.travel
            if travel.name not in rates_summary:
                travel_is = TravelSerializer(travel, context={"request": self.request}).data
                rates_summary[travel.name] = {"travel_is": travel_is, "money_rate": None, "sleep_rate": None}

            rates_summary[travel.name]["sleep_rate"] = sleep_rate.rate

        for travel_name, rates in rates_summary.items():
            combined_rate = {}
            if rates["money_rate"] is not None:
                combined_rate["money_rate"] = rates["money_rate"]
            if rates["sleep_rate"] is not None:
                combined_rate["sleep_rate"] = rates["sleep_rate"]

            rates_summary[travel_name] = {
                "travel_is": rates["travel_is"],
                "rates": combined_rate
            }

        if not rates_summary:
            return Response(
                {"detail": "No ratings found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "rates": rates_summary,
                "Welltravel": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}Welltravel.jpg",
                "Goodpay": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}Goodpay.jpg",
                "Overall": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}Overall.jpg",
            },
            status=status.HTTP_200_OK,
        )


class UserSMRateView(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = UserMiddleRateSerializer
    def get(self,request):
        today = datetime.now().date()
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Authorization token not provided.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        if request.data.get("travel_name"):
            name=request.data.get("travel_name") 
            travel=Travel.objects.filter(name=name).first()
            if not travel:
                return Response(
                {"status":False}, status=status.HTTP_404_NOT_FOUND
            )
            tg=TravellersGroup.objects.filter(travel_is=travel).first()
            if not (
            tg.users.filter(user_id=user.user_id).exists()) and travel.admin!=user:
                return Response({"status":False},status=status.HTTP_403_FORBIDDEN)
            if travel.end_date < today:
                return Response({"status":True},status=status.HTTP_404_NOT_FOUND)
        return Response({"status": False}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request):

        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Authorization token not provided.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Invalid data.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_name_rated = serializer.validated_data["user_name"]
        user_rated = user_model.objects.filter(user_name=user_name_rated).first()
        if not user_rated:
            return Response(
                {"detail": "Rated user not found.", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        travel_name = request.data.get("travel_name")
        travel = Travel.objects.filter(name=travel_name).first()
        if not travel:
            return Response(
                {"detail": "Travel not found."}, status=status.HTTP_404_NOT_FOUND
            )
        group = TravellersGroup.objects.filter(travel_is=travel).first()
        if not group:
            return Response(
                {"detail": "Travel group not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if not (
            group.users.filter(user_id=user.user_id).exists()
            and group.users.filter(user_id=user_rated.user_id).exists())and (travel.admin!=group.travel_is.admin):
            return Response(
                {"detail": "Both users must be in the same group."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if TravelUserRateMoney.objects.filter(
            travel=travel, user_rated=user_rated, rated_by__in=[user]
        ).exists():
            return Response(
                {
                    "error": "You have already rated this user for money.",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if TravelUserRateSleep.objects.filter(
            travel=travel, user_rated=user_rated, rated_by__in=[user]
        ).exists():
            return Response(
                {
                    "error": "You have already rated this user for sleep.",
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_money_rate, _ = TravelUserRateMoney.objects.get_or_create(
            travel=travel, user_rated=user_rated
        )
        user_sleep_rate, _ = TravelUserRateSleep.objects.get_or_create(
            travel=travel, user_rated=user_rated
        )
        user_money_rate.rate = (
            (user_money_rate.rate or 0) * user_money_rate.rated_by.count()
            + serializer.validated_data["rate_money"]
        ) / (user_money_rate.rated_by.count() + 1)
        user_sleep_rate.rate = (
            (user_sleep_rate.rate or 0) * user_sleep_rate.rated_by.count()
            + serializer.validated_data["rate_sleep"]
        ) / (user_sleep_rate.rated_by.count() + 1)

        user_money_rate.rated_by.add(user)
        user_sleep_rate.rated_by.add(user)

        user_money_rate.save()
        user_sleep_rate.save()

        mid_rate = (user_money_rate.rate + user_sleep_rate.rate) / 2
        user_rated.rate = (user_rated.rate or 0) + mid_rate
        user_rated.save()

        return Response(
            {"message": "You rated successfully.", "success": True},
            status=status.HTTP_200_OK,
        )

class UserFullyRateView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Authorization token not provided.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()

        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        money_rates = TravelUserRateMoney.objects.filter(user_rated=user,rate__gt=0)
        sleep_rates = TravelUserRateSleep.objects.filter(user_rated=user,rate__gt=0)
        total_money_rate = TravelUserRateMoney.objects.filter(user_rated=user).aggregate(total_rate=Sum('rate'))['total_rate'] or 0
        total_sleep_rate = TravelUserRateSleep.objects.filter(user_rated=user).aggregate(total_rate=Sum('rate'))['total_rate'] or 0
        total_money = total_money_rate / len(money_rates) if len(money_rates) > 0 else 0
        total_sleep = total_sleep_rate / len(sleep_rates) if len(sleep_rates) > 0 else 0
        rate=(total_money+total_sleep)/2
        return Response({"total":rate,"total_money":total_money,"total_sleep":total_sleep,
                "Welltravel": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}Welltravel.jpg",
                "Goodpay": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}Goodpay.jpg",
                "Overall": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}Overall.jpg",})
class AddTravelUserView(APIView):
    serializer_class = TravelPostGroupSerializer
    authentication_classes = [TokenAuthentication]

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

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()

        if not user:
            return Response(
                {"detail": "User not found.","full":False}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            travel_name = serializer.validated_data["name"]

            travel = Travel.objects.filter(name=travel_name).first()
            tg = TravellersGroup.objects.filter(travel_is=travel).first()
            if not travel:
                return Response(
                    {"detail": "Travel not found.","full":False}, status=status.HTTP_404_NOT_FOUND
                )           
            if travel.empty_travellers >= travel.travellers:
                return Response(
                    {"detail": "This travel is full.","full":True}, status=status.HTTP_400_BAD_REQUEST
                )
            if user == tg.users: 
                return Response({"user":"this user is in travel.","full":False})
            if travel.status == "Private":
                key=request.data.get('key')
                if str(travel.key).strip() != str(key).strip():
                    return Response({"error":"your key is not correct","full":False},status=status.HTTP_403_FORBIDDEN)
            Requests.objects.create(user_request=user, travel=travel,travel_name=travel.name)
            admin = travel.admin
            email = admin.email
            from django.core.mail import send_mail

            send_mail(
                subject="Request to Join Travel",
                message=(
                    f"Hello {admin.user_name},\n\n"
                    f"You have a new request from {user.user_name} to join the travel group '{travel_name}'."
                ),
                from_email="triiptide@gmail.com",
                recipient_list=[email],
                html_message=f"""
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f9f9f9;
                                }}
                                .email-container {{
                                    max-width: 600px;
                                    margin: 20px auto;
                                    background: #ffffff;
                                    border: 1px solid #dddddd;
                                    border-radius: 8px;
                                    overflow: hidden;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                }}
                                .header {{
                                    background-color:#22487a;
                                    color: white;
                                    padding: 20px;
                                    text-align: center;
                                }}
                                .content {{
                                    padding: 20px;
                                    color: #333333;
                                    line-height: 1.6;
                                }}
                                .footer {{
                                    text-align: center;
                                    padding: 10px;
                                    font-size: 12px;
                                    color: #888888;
                                    background-color: #f9f9f9;
                                    border-top: 1px solid #dddddd;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <h1>New Request to Join Travel</h1>
                                </div>
                                <div class="content">
                                    <p>Hello <strong>{admin.user_name}</strong>,</p>
                                    <p>
                                        You have a new request from <strong>{user.user_name}</strong> to join the travel group
                                        <strong>{travel_name}</strong>.
                                    </p>
                                    <p>
                                        Please review the request and take the necessary action.
                                    </p>
                                </div>
                                <div class="footer">
                                    <p>&copy; TripTide Team</p>
                                </div>
                            </div>
                        </body>
                    </html>
                """,
            )

            return Response(
                {"detail": "Your request has been sent to the admin.","full":False},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RequestView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_user_from_token(self, token):
        """Helper method to decode JWT token and fetch the user."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload.get("user_id")).first()

        if not user:
            raise AuthenticationFailed("User not found.")
        return user
        if BlacklistedToken.objects.filter(token=token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
    def get(self, request):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        user = self.get_user_from_token(user_token)

        requests_to_add = Requests.objects.filter(travel__admin=user)
        if not requests_to_add.exists():
            return Response(
                {"detail": "There are no requests."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RequestSerializer(requests_to_add, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user.")

        user = self.get_user_from_token(user_token)

        is_accept = request.data.get("is_accept")
        travel_name = request.data.get("travel_name")
        user_name = request.data.get("user_name")

        if not (travel_name and user_name):
            return Response(
                {"detail": "Travel name and user name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_add = get_user_model().objects.get(user_name=user_name)
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": "The specified user does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        travel = Travel.objects.filter(name=travel_name).first()
        if not travel:
            return Response(
                {"detail": "This travel does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if travel.admin != user:
            return Response(
                {"detail": "You are not the admin of this travel."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if is_accept == "True":
            if travel.empty_travellers >= travel.travellers:
                return Response(
                    {"detail": "This travel is full."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
            travel.empty_travellers += 1
            travel.save()

            tg, created = TravellersGroup.objects.get_or_create(travel_is=travel)
            tg.users.add(user_add)
            tg.save()


            TravelUserRateMoney.objects.create(travel=travel, user_rated=user_add)
            TravelUserRateSleep.objects.create(travel=travel, user_rated=user_add)

            request_record = Requests.objects.filter(
                user_request=user_add, travel__name=travel_name
            ).first()
            if request_record:
                request_record.delete()
            send_mail(
                subject="Request Approved",
                message=(
                    f"Hello {user_add.user_name},\n"
                    f"You have been accepted into travel '{travel_name}'."
                ),
                from_email="triiptide@gmail.com",
                recipient_list=[user_add.email],
                html_message=f"""
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 0;
                                    padding: 0;
                                    background-color: #f4f4f9;
                                }}
                                .email-container {{
                                    max-width: 600px;
                                    margin: 20px auto;
                                    background: #ffffff;
                                    border: 1px solid #dddddd;
                                    border-radius: 8px;
                                    overflow: hidden;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                }}
                                .header {{
                                    background-color: #22487a;
                                    color: white;
                                    padding: 20px;
                                    text-align: center;
                                }}
                                .content {{
                                    padding: 20px;
                                    color: #333333;
                                    line-height: 1.6;
                                }}
                                .footer {{
                                    text-align: center;
                                    padding: 10px;
                                    font-size: 12px;
                                    color: #888888;
                                    background-color: #f4f4f9;
                                    border-top: 1px solid #dddddd;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <h1>Request Approved</h1>
                                </div>
                                <div class="content">
                                    <p>Hello <strong>{user_add.user_name}</strong>,</p>
                                    <p>
                                        Congratulations! You have been accepted into the travel group 
                                        <strong>{travel_name}</strong>.
                                    </p>
                                    <p>
                                        We are excited to have you join us and hope you have an amazing journey!
                                    </p>
                                </div>
                                <div class="footer">
                                    <p>&copy; TripTide Team</p>
                                </div>
                            </div>
                        </body>
                    </html>
                """,
            )


            return Response(
                {"detail": "User added to the group."}, status=status.HTTP_200_OK
            )
        request_record = Requests.objects.filter(
            user_request=user_add, travel__name=travel_name
        ).first()
        if request_record:
            request_record.delete()

        return Response(
            {"detail": "You have not accepted the request."}, status=status.HTTP_200_OK
        )
    def delete(self, request):
        cutoff_date = now() - timedelta(days=10)
        deleted_count, _ = Requests.objects.filter(created_at__lt=cutoff_date).delete()

        return Response(
            {"message": f"Deleted {deleted_count} old request(s) successfully."},
            status=status.HTTP_200_OK,
        )
class RateByMeView(APIView):
    def get(self,request):
        today = datetime.now().date()
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise AuthenticationFailed("Authorization token not provided.")

        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload["user_id"]).first()
        if not user:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if BlacklistedToken.objects.filter(token=user_token).exists():
            return Response("Token has been invalidated.",status=status.HTTP_403_FORBIDDEN)
        travel_name=request.query_params.get("travel_name")
        if not travel_name:
            return Response("travelname is required",status=status.HTTP_400_BAD_REQUEST)
        travel=Travel.objects.filter(name=travel_name).first()
        if not travel:
            return Response("travel does not exit",status=status.HTTP_404_NOT_FOUND)
        user_name_rated=request.query_params.get("user_name")
        if not user_name_rated:
            return Response("username is required",status=status.HTTP_400_BAD_REQUEST)
        user_rated = user_model.objects.filter(user_name=user_name_rated).first()
        if not user_rated:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        money_rates=TravelUserRateMoney.objects.filter(travel=travel,rated_by=user,user_rated=user_rated).first()
        sleep_rates=TravelUserRateSleep.objects.filter(travel=travel,rated_by=user,user_rated=user_rated).first()
        monyes=MyRatedOtherMoneySerializer(money_rates).data
        sleeps=MyRatedOtherSleepSerializer(sleep_rates).data
        return Response({'money':monyes,'sleep':sleeps},status=status.HTTP_200_OK)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    