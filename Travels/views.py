from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Travel, EmailAddress, TravellersGroup, UserRate
from .serializers import (
    TravelSerializer,
    EmailSerializer,
    TravelGroupSerializer,
    TravelPostGroupSerializer,
    TravelPostSerializer,
    UserRateSerializer,
    TravelRateSerializer,
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

class AllTravels(generics.ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = [
        "travellers",
        "admin__user_name",
        "mode",
        "destination",
        "transportation",
        "start_place",
        "start_date__month",
    ]
    filterset_fields = ("travellers", "admin__user_name", "mode")


class TravelViewSpring(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        spring_travel = queryset.filter(start_date__month__in=[1, 2, 3])
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
        winter_travel = queryset.filter(start_date__month__in=[10, 11, 12])
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
        autumn_travel = queryset.filter(start_date__month__in=[7, 8, 9])
        autumn_serializer = TravelSerializer(
            autumn_travel, many=True, context={"request": self.request}
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
        summer_travel = queryset.filter(start_date__month__in=[4, 5, 6])
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

    def get(self, request, pk):
        try:
            travel_get = Travel.objects.get(pk=pk)
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
        return Response(data=travel_serializer.data, status=status.HTTP_200_OK)


class TravelGroupView(APIView):
    serializer_class = TravelGroupSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # user_token = request.COOKIES.get("access_token")
        user_token = request.headers.get('Authurization')
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
        travel_admin=Travel.objects.filter(admin=user)
        user_groups = TravellersGroup.objects.filter(
        Q(users=user) | Q(travel_is__in=travel_admin)
        )


        if user_groups.exists():
            serializer = TravelGroupSerializer(
                user_groups, many=True, context={"request": self.request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "No travel groups found for the user."},
            status=status.HTTP_404_NOT_FOUND,
        )


class AddTravelUserView(APIView):
    serializer_class = TravelPostGroupSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user_token = request.COOKIES.get("access_token")
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

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            travel_name = serializer.validated_data["name"]
            travel = Travel.objects.filter(name=travel_name).first()

            if not travel:
                return Response(
                    {"detail": "Travel not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            elif travel.empty_travellers < travel.travellers:
                travel.empty_travellers += 1
                travel.save()
                tg, created = TravellersGroup.objects.get_or_create(travel_is=travel)
                tg.users.add(user)
                return Response(
                    {"detail": "Travel successfully booked."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"detail": "This travel is full."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostTravelView(APIView):
    serializer_class = TravelPostSerializer
    authenticated_classes = [TokenAuthentication]
    def post(self, request):
        user_token = request.COOKIES.get("access_token")
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
        serializer=TravelPostSerializer(data=request.data)
        if serializer.is_valid():
            travel =  serializer.save(admin=user,photo=request.data.get('photo'))
            TravellersGroup.objects.create(travel_is=travel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class UserRateView(APIView):
    serializer_class = UserRateSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user_token = request.COOKIES.get("access_token")
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

        rate = user.rate
        return Response({"rate": rate}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_token = request.COOKIES.get("access_token")
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

        serializer = UserRateSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['user_name']
            rate_add = serializer.validated_data['rate']
            if rate_add>5 or rate_add<0:
                return Response("the rate should be 0 to 5")
            add_rate_user = User.objects.filter(user_name=username).first()

            if not add_rate_user:
                return Response({"detail": "User to rate not found."}, status=status.HTTP_404_NOT_FOUND)

            rate_user, created = UserRate.objects.get_or_create(user=add_rate_user)
            if user in rate_user.rated_by.all():
                return Response({"detail": "You have already rated this user."}, status=status.HTTP_400_BAD_REQUEST)

            rate_user.rated_by.add(user)
            rate_user.number_rated_by += 1

            rated=add_rate_user.rate+rate_add

            add_rate_user.rate = rated / rate_user.number_rated_by

            add_rate_user.save()
            rate_user.save()

            return Response(f"You rated {username} successfully.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TravelRateView(APIView):
    serializer_class = TravelRateSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user_token = request.COOKIES.get("access_token")
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


        serializer = TravelRateSerializer(data=request.data)
        if serializer.is_valid():
            travel_name = serializer.validated_data[
                "travel_name"
            ]  
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

            is_part_of_group = group.users.filter(user_id=user.user_id).exists()
            is_admin = travel.admin == user

            if not (is_part_of_group or is_admin):
                return Response(
                    {"detail": "User is not authorized to rate this travel."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if travel.rated_by_user.filter(pk=user.pk).exists():
                return Response({"error": "You have already rated this travel."}, status=status.HTTP_400_BAD_REQUEST)

            total_rate = travel.rate * travel.rated_by  
            total_rate += serializer.validated_data["rate"]  
            travel.rated_by += 1  
            travel.rate = total_rate / travel.rated_by 
            travel.rated_by_user.add(user)
            travel.save()

            return Response({"success": "You rated successfully."})

        return Response(
            {"error": "Your input data is invalid."}, status=status.HTTP_400_BAD_REQUEST
        )
