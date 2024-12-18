from django.urls import path
from .views import *
from . import consumers
from .views_consumer import AblyMessagePublishView
urlpatterns = [
    path("chat/messages/",ChatMessageView.as_view()),
    path('publish_message/', AblyMessagePublishView, name='publish_message'),
]
