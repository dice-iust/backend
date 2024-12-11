from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:travel_name>/', consumers.ChatConsumer.as_asgi()),
]
