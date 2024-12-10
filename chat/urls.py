from django.urls import path
from .views import *

urlpatterns = [
    path("chat/<str:travel_name>/messages/",ChatMessageView.as_view()),
]
