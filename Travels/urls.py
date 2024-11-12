from django.urls import path
from .views import TravelView
urlpatterns = [ path("travels/",TravelView.as_view()),
]
