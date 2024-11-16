from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Travel
from .serializers import TravelSerializer
from datetime import datetime, timedelta
from django.db.models import F, ExpressionWrapper, DurationField, Q
from calendar import monthrange
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

User = get_user_model()


class TravelFilter(filters.FilterSet):
    travellers = filters.NumberFilter(field_name="travellers", lookup_expr="exact")
    admin = filters.CharFilter(field_name="admin__user_name", lookup_expr="icontains")
    destination = filters.CharFilter(field_name="destination", lookup_expr='exact')
    start_place = filters.CharFilter(field_name="start_place", lookup_expr='exact')
    transportation = filters.CharFilter(field_name="transportation",lookup_expr='exact')
    mode=filters.ChoiceFilter(field_name="mode")
    class Meta:
        model = Travel
        fields = ["travellers","admin", "destination", "transportation",'mode']


class AllTravels(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TravelFilter
    
    def get(self,request):
        querysets=Travel.objects.all()
        serializer=TravelSerializer(querysets,many=True,context={"request": request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    
    
    
    
class TravelView(ListAPIView):
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = datetime.now()
        last_day_of_month = datetime(
            today.year, today.month, monthrange(today.year, today.month)[1]
        )

        queryset = self.filter_queryset(self.get_queryset())
        popular_travel = queryset.order_by("-travellers")[:15]
        fancy_travel = queryset.filter(mode="Fancy")
        budget_travel = queryset.filter(mode="budget")
        upcoming_travel = queryset.filter(
            start_date__gte=today, start_date__lte=last_day_of_month
        )
        quick_travel = queryset.annotate(
            duration=ExpressionWrapper(
                F("end_date") - F("start_date"), output_field=DurationField()
            )
        ).filter(Q(duration=timedelta(days=2)) | Q(duration=timedelta(days=1)))

        spring_travel = queryset.filter(start_date__month__in=[1, 2, 3])
        summer_travel = queryset.filter(start_date__month__in=[4, 5, 6])
        autumn_travel = queryset.filter(start_date__month__in=[7, 8, 9])
        winter_travel = queryset.filter(start_date__month__in=[10, 11, 12])

        context = {
            "Popular": TravelSerializer(
                popular_travel, many=True, context={"request": self.request}
            ).data,
            "Fancy": TravelSerializer(
                fancy_travel, many=True, context={"request": self.request}
            ).data,
            "BudgetFriendly": TravelSerializer(
                budget_travel, many=True, context={"request": self.request}
            ).data,
            "Upcoming": TravelSerializer(
                upcoming_travel, many=True, context={"request": self.request}
            ).data,
            "Quick": TravelSerializer(
                quick_travel, many=True, context={"request": self.request}
            ).data,
            "Spring": TravelSerializer(
                spring_travel, many=True, context={"request": self.request}
            ).data,
            "Summer": TravelSerializer(
                summer_travel, many=True, context={"request": self.request}
            ).data,
            "Autumn": TravelSerializer(
                autumn_travel, many=True, context={"request": self.request}
            ).data,
            "Winter": TravelSerializer(
                winter_travel, many=True, context={"request": self.request}
            ).data,
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
