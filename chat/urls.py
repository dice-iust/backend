from django.urls import path
from .views import *
from . import consumers

urlpatterns = [
    path("chat/<str:travel_name>/messages/",ChatMessageView.as_view()),
]
