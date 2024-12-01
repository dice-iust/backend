from django.urls import path
from .views import *
urlpatterns = [ 
    path("travels/",TravelViewPopular.as_view()),
    path("travels/<int:pk>/",SingleTravelView.as_view()),
    path('travels/filter/',AllTravels.as_view()),
    path("travels/spring/",TravelViewSpring.as_view()),
    path("travels/summer/",TravelViewSummer.as_view()),
    path("travels/winter/",TravelViewWinter.as_view()),
    path("travels/autumn",TravelViewAutumn.as_view()),
    path("travels/fancy/",TravelViewFancy.as_view()),
    path("travels/upcoming/",TravelViewUpcoming.as_view()),
    path("travels/short/",TravelViewShort.as_view()),
    path("travels/economy/",TravelVieweconomy.as_view()),
    path("travels/add/",PostTravelView.as_view()),
    path('email/',EmailView.as_view()),
    path('mytravels/',TravelGroupView.as_view()),
    path("travels/adduser/",AddTravelUserView.as_view()),
    path('myrate/',UserRateView.as_view()),path("travels/rating",TravelRateView.as_view()),
    path('travels/users/rate/',TravelUserRateView.as_view()),
]

