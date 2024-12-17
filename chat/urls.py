from django.urls import path
from .views import *
from . import consumers
from .views_consumer import AblyMessagePublishView
urlpatterns = [
    path("chat/<str:travel_name>/messages/",ChatMessageView.as_view()),
    path('publish_message/', AblyMessagePublishView, name='publish_message'),
]
