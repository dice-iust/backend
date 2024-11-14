from django.urls import path
from .views import TravelView,SingleTravelView,TravelMakeView
urlpatterns = [ 
    path("travels/",TravelView.as_view()),
    path("travels/<int:pk>",SingleTravelView.as_view())
]
