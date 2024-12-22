# from django.urls import path
# from .views import *
from . import consumers
from .views_consumer import AblyMessagePublishView
# urlpatterns = [
#     path("chat/messages/",ChatMessageView.as_view()),
#     path('publish_message/', AblyMessagePublishView, name='publish_message'),
# ]
from django.urls import path
from .views_consumer import post_message, message_stream

urlpatterns = [
    path('api/chat/message/', post_message, name='post_message'),
    path('events/chat/<str:travel_name>/', message_stream, name='message_stream'),
    path('publish_message/', AblyMessagePublishView, name='publish_message'),
]
