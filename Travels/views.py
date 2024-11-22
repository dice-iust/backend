from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Travel
from .serializers import TravelSerializer,EmailSerializer
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

User = get_user_model()


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
        'start_place','start_date__month'
    ]
    filterset_fields = ("travellers",'admin__user_name','mode')


class TravelViewSpring(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        spring_travel = queryset.filter(start_date__month__in=[1, 2, 3])

        context = {
            "Spring Trips": TravelSerializer(
                spring_travel, many=True, context={"request": self.request}
            ).data,
            "photo_spring": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/SpringTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)


class TravelViewWinter(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        winter_travel = queryset.filter(start_date__month__in=[10,11,12])

        context = {
            "Winter Trips": TravelSerializer(
                winter_travel, many=True, context={"request": self.request}
            ).data,
            "photo_winter": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/WinterTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)


class TravelViewAutumn(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        autumn_travel = queryset.filter(start_date__month__in=[7,8,9])

        context = {
            "Autumn Trips": TravelSerializer(
                autumn_travel, many=True, context={"request": self.request}
            ).data,
            "photo_autumn": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/AutumnTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)


class TravelViewSummer(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        summer_travel = queryset.filter(start_date__month__in=[4,5,6])

        context = {
            "Summer Trips": TravelSerializer(
                summer_travel, many=True, context={"request": self.request}
            ).data,
            "photo_summer": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/SummerTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)

class TravelViewFancy(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        fancy_travel = queryset.filter(mode="Fancy")
        context = {
            "Fancy Trips": TravelSerializer(
                fancy_travel, many=True, context={"request": self.request}
            ).data,
            "photo_fancy": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/FancyTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)
class TravelVieweconomy(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        fancy_travel = queryset.filter(mode="Budget-friendly")
        context = {
            "economival Trips": TravelSerializer(
                fancy_travel, many=True, context={"request": self.request}
            ).data,
            "photo_economy": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/economicalTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)

class TravelViewPopular(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Travel.objects.all()
        popular_travel = queryset.order_by("-travellers")[:15]
        context = {
            "Popular Trips": TravelSerializer(
                popular_travel, many=True, context={"request": self.request}
            ).data,
            "photo_spring": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/SpringTrips.avif",
            "photo_winter": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/WinterTrips.avif",
            "photo_autumn": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/AutumnTrips.avif",
            "photo_summer": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/SummerTrips.avif",
            "photo_fancy": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/FancyTrips.avif",
            "photo_economy": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/economicalTrips.avif",
            "photo_upcoming": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/UpcomingTrips.avif",
            "photo_short": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/ShortTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)
    
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
        context = {
            "Up comingTrips": TravelSerializer(
                upcoming_travel, many=True, context={"request": self.request}
            ).data,
            "photo_upcoming": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/Upcomingtrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)


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

        context = {
            "Short Trips": TravelSerializer(
                quick_travel, many=True, context={"request": self.request}
            ).data,
            "photo_short": f"https://triptide.pythonanywhere.com{settings.MEDIA_URL}travels/ShortTrips.avif",
        }
        return Response(data=context, status=status.HTTP_200_OK)


class SingleTravelView(APIView):
    serializer_class = TravelSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            travel_get = Travel.objects.get(pk=pk)
        except Travel.DoesNotExist:
            return Response(
                {"detail": "This travel does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        travel_serializer = TravelSerializer(travel_get, context={"request": request})
        return Response(data=travel_serializer.data, status=status.HTTP_200_OK)
