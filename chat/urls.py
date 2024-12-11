from django.urls import path
from .views import *

urlpatterns = [
    path("chat/<str:travel_name>/messages/",ChatMessageView.as_view()),
]
from django.urls import re_path
from .consumers import ChatConsumer  # Ensure this points to your consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<travel_name>\w+)/$',ChatConsumer.as_asgi()),
]
